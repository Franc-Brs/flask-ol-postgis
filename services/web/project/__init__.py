from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from .models import db, City
import geoalchemy2.functions as func
import json
from werkzeug.utils import secure_filename
from sqlalchemy import select
import os

app = Flask(__name__)
app.config.from_object("project.config.Config")
app.secret_key = "secret key"
#db = SQLAlchemy(app)
db.init_app(app)

from .functions import allowed_file

@app.route("/<int:celsius>")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    
    fahrenheit = float(celsius) * 9 / 5 + 32
    fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
    return str(fahrenheit)

@app.route('/maps')
def root_ol():
   markers=[
       {
        'lat':0,
        'lon':0,
        'popup':'Null Island - just test popup'
        }
   ]
   return render_template('map_ol.html', markers=markers)

@app.route('/points_geom', methods=['GET'])
def get_all_points():
    """
    only geometries 
    """
    cities = City.query.all()
    results = [
                {
                    "type": "Feature",
                    "geometry": json.loads(db.session.scalar(func.ST_AsGeoJSON(city.geo))),
                    "properties": {}  
                } for city in cities
    ]
    
    layer = {
        "type":"FeatureCollection",
        "features": results
    }

    return jsonify(layer)

@app.route('/geojson', methods=['GET'])
def test():
    """
    geojson 
    """
    # quick and dirty but I was in a hurry
    #query_geo= db.engine.execute(f"SELECT ST_AsGeoJSON(t.*) FROM {City.__tablename__} AS t;")
    #results = [ json.loads((row[0])) for row in query_geo ]
    
    select_stmt = select([func.ST_AsGeoJSON(City, 'geo')])
    query_all = db.engine.execute(select_stmt).scalars().all()

    results = [ json.loads(row) for row in query_all ]

    layer = {
        "type":"FeatureCollection",
        "features": results,
    }
    
    return jsonify(layer)


@app.route('/upload', methods=['POST','GET'])
def upload_file():
    
    if request.method == 'POST':
        # check if the post request has the file part
        #files = request.files.getlist("file[]")
        #for f in files:
        #    print(f)
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
          
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/upload')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    
    return render_template('upload.html')

