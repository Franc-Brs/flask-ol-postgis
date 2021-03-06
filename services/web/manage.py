
from flask.cli import FlaskGroup
from project import create_app, ext_celery
#from project.models import City
import click
from project.api.models import City

app = create_app()
celery = ext_celery.celery
cli = FlaskGroup(app)

@cli.command("random_data")
def add_cities_hc():
    City.add_city("Sausalito", -122.4853, 37.8591)
    City.add_city("Daly City", -122.4702, 37.6879)
    City.add_city("San Jose", -121.8863, 37.3382)
    City.add_city("Vallejo", -122.2566, 38.1041)
    City.add_city("Orlando", -81.3815, 28.5469)
    City.add_city("New York City", -73.9603, 40.7666)

@cli.command("costum_city")
@click.argument("Name", nargs=1)
@click.argument("lat", nargs=1)
@click.argument("lon", nargs=1)
def add_costum_city(name, lon, lat):
    City.add_city(name, lon, lat)   

if __name__ == "__main__":
    cli()