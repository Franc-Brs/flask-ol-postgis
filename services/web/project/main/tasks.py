from celery import shared_task

@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

import geopandas as gpd
from project.api.models import db, File, status_type
import os

@shared_task
def import_in_db():
    """
    todo: check File db (status based) and load shp into postgis
    """
    # add try excpet where except make the task be run another time
    shp_files = File.query.filter(File.status == status_type.UPLOADED, File.name.like('%.shp')).all()
    for file in shp_files:

        shp_file = gpd.read_file(file.fp)
        dir_name = os.path.dirname(file.fp)
        #change column name in not-capitalized letters and name wihtout extension
        shp_file.to_postgis(name=file.name,con=db.engine)

        file.status = status_type.SENT_TO_DB

        other_files = File.query.filter(File.status == status_type.UPLOADED, 
                                        File.name.notlike('%.shp'),
                                        File.fp.like(f"{dir_name}%")).all()
        
        for other_file in other_files:
            other_file.status = status_type.SENT_TO_DB
        
        db.session.commit()
    return 