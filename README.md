# 🚩 Table of Contents
- [Brief description](#brief-description)
- [Required](#required)
- [Quickstart](#quickstart)
- [Test data](#test-data)
- [Other Useful Links and TODO](#other-useful-links-and-todo)
## Brief description
Basic stack to build a really simple webgis:
* Flask as a backend
* Postgres/Postgis as database
* Openlayers for displaying the data
Everything is dockerized; it is, by the way, just a 🧪 test 🧪.
## Required
* Docker
* Docker-compose

## Quickstart
Take the structure from [Michael Herman post](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/), this is a simple test: not production ready! Read the post from Micheal Herman if you are interested in that, I tried to keep it simple.
Clone the repository, to run the app: 
```
docker-compose up -d
```
Now it should be possibile to navigate to http://localhost:5000/maps/ and see something like this:

<p align="center">
<img src="https://user-images.githubusercontent.com/79576081/172322299-5311ec66-a5d5-4f5c-812c-da6d19209e55.png" height="400">
</p>

Useful links for Openlayers:
* https://openlayers.org/en/latest/doc/quickstart.html
* https://openstreetmap.be/en/projects/howto/openlayers.html
* https://openlayers.org/en/latest/examples/icon.html

At http://localhost:5000/api/point_geom and http://localhost:5000/api/geojson the points in the db should be available in form of geojson.

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
docker-compose exec web python manage.py costum_city Milano 45.458561447284616 9.187270434306852
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
I took data and db model from [Jennifer Blog](https://www.jennifergd.com/post/7/). Only a [reminder](https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045).

If the db is populated as explaind it should be possibile to see some points:

<p align="center">
<img src="https://user-images.githubusercontent.com/79576081/172825755-f6872f15-c025-4ac0-a117-9ab17f6b3c62.png" height="400">
</p>

At the moment onlly points can be added (in OpenLayers), but the api expose every type of geometry as geoJSON.

## File uploads

You can navigate to http://localhost:5000/application/uploads upload a file or a group of files (at the moment only shp)

<p align="center">
<img src="https://user-images.githubusercontent.com/79576081/173757730-832d224a-9cf8-4130-aaa2-4135de0882a4.png" height="250">
</p>

## Other Useful Links and TODO

I tried to use Flask-Migrate but I had some issue with Postgis (Geometry column) table, I followed [this link](https://github.com/miguelgrinberg/Flask-Migrate/issues/18) and [this gist](https://gist.github.com/utek/6163250) and I modified `env.py` and `alembic.ini` accordingly.
I also added one line to `script.py.mako`:
```python
import geoalchemy2
```
And I downgraded the version of GeoAlchemy in order to create the table according to [this issue](https://github.com/geopandas/geopandas/issues/2375).
TODO: I should re-write a little bit the migrate and upgrade part in `services\web\entrypoint.sh`. If some troubles with the db is encountered the issue can be solved with:
```
docker-compose build && bdocker-compose up -d
```


