
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geoalchemy2 import Geometry

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

class City(db.Model):
    """A city, including its geospatial data. - thks https://www.jennifergd.com/post/7/"""

    __tablename__ = "cities"

    point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(30))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    geo = db.Column(Geometry(geometry_type="POINT"))

    def __repr__(self):
        return "<City {name} ({lat}, {lon})>".format(
            name=self.location, lat=self.latitude, lon=self.longitude)
    """
    def get_cities_within_radius(self, radius):
        #Return all cities within a given radius (in meters) of this city.

        return City.query.filter(func.ST_Distance_Sphere(City.geo, self.geo) < radius).all()
    """
    @classmethod
    def add_city(cls, location, longitude, latitude):
        """Put a new city in the database."""

        geo = 'POINT({} {})'.format(longitude, latitude)
        city = City(location=location,
                           longitude=longitude,
                           latitude=latitude,
                          geo=geo)

        db.session.add(city)
        db.session.commit()

    @classmethod
    def update_geometries(cls):
        """Using each city's longitude and latitude, add geometry data to db."""

        cities = City.query.all()

        for city in cities:
            point = 'POINT({} {})'.format(city.longitude, city.latitude)
            city.geo = point

        db.session.commit()