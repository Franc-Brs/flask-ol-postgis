Tak the structure from here:

https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

To run the app: docker-compose up -d.
As an example to user the flask-cli I added a functio to add costum user email to the db.
Once the containers are up, simply run:

```
docker-compose exec web python manage.py seed_db <example@org>
```

To show leaflet I used https://medium.com/geekculture/how-to-make-a-web-map-with-pythons-flask-and-leaflet-9318c73c67c3

Show OpenLayers map (search quick start OpenLayers) and popup: https://openstreetmap.be/en/projects/howto/openlayers.html
marker and popup https://openlayers.org/en/latest/examples/icon.html

Can it be useful? https://muetsch.io/serving-raster-data-from-postgis-as-wms-using-python-and-fastapi-or-flask.html
https://www.jennifergd.com/post/7/
https://www.big-meter.com/opensource/en/61db085731176a72587a2584.html

Db and models https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
