from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .models import db

app = Flask(__name__)
app.config.from_object("project.config.Config")
#db = SQLAlchemy(app)
db.init_app(app)

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/<int:celsius>")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    
    fahrenheit = float(celsius) * 9 / 5 + 32
    fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
    return str(fahrenheit)

@app.route("/vedi")
def template_test():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])

@app.route('/map_ol')
def root_ol():
   markers=[
       {
        'lat':0,
        'lon':0,
        'popup':'Null Island - just test popup'
        }
   ]
   return render_template('map_ol.html', markers=markers)