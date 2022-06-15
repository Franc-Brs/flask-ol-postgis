
from . import api_blueprint
from flask import render_template, jsonify
from .models import db, City
import geoalchemy2.functions as func
import json
from sqlalchemy import select
"""
@api_blueprint.route('/')
def index():
    return render_template('users/index.html')
"""

@api_blueprint.route('/point_geom', methods=['GET'])
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


@api_blueprint.route('/geojson', methods=['GET'])
def test():
    
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

