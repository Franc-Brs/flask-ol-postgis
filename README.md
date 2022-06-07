# 🚩 Table of Contents
- [Required](#required)
- [Quickstart](#quickstart)
- [Test data](#test-data)
- [Other Useful Links](#other-useful-links)
## Required
* Docker
* Docker-compose

## Quickstart
Take the structure from [Michael Herman post](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/), this is a simple test: not production ready! Read the post from Micheal Herman if you are interested in that, I tried to keep it simple.
Clone the repository, to run the app: 
```
docker-compose up -d
```
Now it should be possibile to navigate to http://localhost:5000/map_ol and see something like this:

<p align="center">
<img src="https://user-images.githubusercontent.com/79576081/172322299-5311ec66-a5d5-4f5c-812c-da6d19209e55.png" height="400">
</p>

Useful links for Openlayers:
* https://openlayers.org/en/latest/doc/quickstart.html
* https://openstreetmap.be/en/projects/howto/openlayers.html
* https://openlayers.org/en/latest/examples/icon.html

## Test data
In order to populate the PostgreSQL/PostGIS db some hardcoded test data can be used.
Once the containers are up, simply run:
```
docker-compose exec web python manage.py random_data
```
Or, if you want to add some costum city:
```
docker-compose exec web python manage.py costum_city <Name of the city> <lat in WGS84> <lon in WGS84>
```
For example:
```
docker-compose exec web python manage.py costum_city <Milano 45.458561447284616 9.187270434306852
```
After having created a record you can check the db with psql, access the cli:
```
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
```
And check if the cities has been added:
```
hello_flask_dev=# select * from cities;
```
The ouput should be something similiar:
```
 point_id |   location    |     longitude     |      latitude      |                    geo
----------+---------------+-------------------+--------------------+--------------------------------------------
        1 | Sausalito     |         -122.4853 |            37.8591 | 0101000000EC2FBB270F9F5EC02EFF21FDF6ED4240
        2 | Daly City     |         -122.4702 |            37.6879 | 010100000012A5BDC1179E5EC08E75711B0DD84240
        3 | San Jose      |         -121.8863 |            37.3382 | 0101000000789CA223B9785EC0ECC039234AAB4240
        4 | Vallejo       |         -122.2566 |            38.1041 | 0101000000D50968226C905EC0BEC11726530D4340
        5 | Orlando       |          -81.3815 |            28.5469 | 010100000023DBF97E6A5854C0B22E6EA3018C3C40
        6 | New York City |          -73.9603 |            40.7666 | 01010000005396218E757D52C08A8EE4F21F624440
        7 | Milano        | 9.187270434306852 | 45.458561447284616 | 010100000017B60DE9E15F22409DA53924B2BA4640
```
I took data and db model from [Jennifer Blog](https://www.jennifergd.com/post/7/). Only a [reminder](https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045)

## Other Useful Links
* https://muetsch.io/serving-raster-data-from-postgis-as-wms-using-python-and-fastapi-or-flask.html
* https://www.big-meter.com/opensource/en/61db085731176a72587a2584.html
 
