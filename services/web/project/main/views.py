
from . import main_blueprint
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os
from flask import current_app
from .functions import allowed_file
from flask_log_request_id import current_request_id

from project.api.models import db, File

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

                file.save(os.path.join(temp_path, filename))
                flash(f"{file.filename} successfully uploaded", 'info')
            else:
                flash(f"{file.filename} cannot be uploaded: allowed file types are {current_app.config['ALLOWED_EXTENSIONS']}",'warning')
    
        return redirect(request.url)
    #flash(f"{current_request_id()}")
    return render_template('main/uploads.html')