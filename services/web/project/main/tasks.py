from celery import shared_task

@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

import geopandas as gpd
from project.api.models import db, File

@shared_task
def import_in_db():
    """
    todo: check File db (status based) and load shp into postgis
    """
    import time
    time.sleep(5)
    shp_file = gpd.read_file('/usr/src/app/uploads/56f680c2-1a87-4c26-b560-812dc836d490/prov2011_g.shp')
    #change column name in not-capitalized letters
    shp_file.to_postgis(name='province',con=db.engine)
    #with current_app.app_context():
    #for file in File.query.all():
    #    print(file.fp)
    return 