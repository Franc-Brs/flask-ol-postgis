from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .models import db, City
import geoalchemy2.functions as func

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

@app.route('/points', methods=['GET'])
def get_all_points():

    cities = City.query.all()
    results = [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates":
                        [
                            db.session.scalar(func.ST_X(city.geo)),
                            db.session.scalar(func.ST_Y(city.geo))
                        ]
                    },
                    "properties":{
                        "name": city.location,
                        "id": city.point_id
                    }  
                } for city in cities
    ]
    
    layer = {
        "type":"FeatureCollection",
        "features": results
    }
    return jsonify(layer)
    
