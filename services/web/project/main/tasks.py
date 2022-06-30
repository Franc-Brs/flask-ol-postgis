from celery import shared_task

@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

import geopandas as gpd
from project.api.models import db

@shared_task
def import_in_db(x, y):
    import time
    time.sleep(5)
    shp_file = gpd.read_file('./uploads/prov2011_g.shp')
    #change column name in not-capitalized letters
    shp_file.to_postgis(name='province',con=db.engine)
    return x / y