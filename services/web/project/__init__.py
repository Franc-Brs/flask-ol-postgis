from flask import Flask, jsonify, render_template, request
from .models import db, City
import geoalchemy2.functions as func
import json

from sqlalchemy.orm import registry

app = Flask(__name__)
app.config.from_object("project.config.Config")
#db = SQLAlchemy(app)
db.init_app(app)

@app.route("/<int:celsius>")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    
    fahrenheit = float(celsius) * 9 / 5 + 32
    fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
    return str(fahrenheit)

@app.route('/')
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
    query_geo= db.engine.execute(f"SELECT ST_AsGeoJSON(t.*) FROM {City.__tablename__} AS t;")

    results = [ json.loads((row[0])) for row in query_geo ]

    layer = {
        "type":"FeatureCollection",
        "features": results,
    }
    
    return jsonify(layer)