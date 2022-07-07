
from . import main_blueprint
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os
from flask import current_app
from .functions import allowed_file, check_shp
from project.main.tasks import divide, import_in_db # TODO delete 
from flask_log_request_id import current_request_id

from project.api.models import db, File, status_type

@main_blueprint.route('/maps')
def root_ol():
   markers=[
       {
        'lat':0,
        'lon':0,
        'popup':'Null Island - just test popup'
        }
   ]
   return render_template('main/map_ol.html', markers=markers)


@main_blueprint.route('/uploads', methods=['POST','GET'])
def uploads_file():
    
    if request.method == 'POST':
        
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
          
        files = request.files.getlist('files[]')
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_request_id())

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                os.mkdir(temp_path) if not os.path.isdir(temp_path) else None
                save_file_path= os.path.join(temp_path, filename)
                file.save( save_file_path )
                new_file = File(name=filename, fp=os.path.abspath(save_file_path), status=status_type.UPLOADED)
                db.session.add(new_file)
                db.session.commit()
                
                flash(f"{file.filename} successfully uploaded", 'info')
            else:
                flash(f"{file.filename} cannot be uploaded: allowed file types are {current_app.config['ALLOWED_EXTENSIONS']}",'warning')
        
        #it should trigger once all the files are uploaded and only if the folder containing the files exist # TODO delete 
        #task = divide.delay(1, 2) if os.path.isdir(temp_path) else None # TODO delete 
        if check_shp(temp_path):
            task = import_in_db.delay() if os.path.isdir(temp_path) else None # TODO delete 
        else:
            #TODO remove the folder if entering here
            flash(f"Some files has been missing in the upload (.shp, .dbf and .shx should be uploaded), \
                    retry to upload all the necessary files", 'error_upload')

        return redirect(request.url)
         
    return render_template('main/uploads.html')