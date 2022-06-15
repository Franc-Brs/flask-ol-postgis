
from . import main_blueprint
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os
from flask import current_app
from .functions import allowed_file

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
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                flash(f"{file.filename} successfully uploaded")
            else:
                flash(f"*** {file.filename} cannot be uploaded: allowed file types are {current_app.config['ALLOWED_EXTENSIONS']} ***")
    
        return redirect(request.url)
    
    return render_template('main/uploads.html')