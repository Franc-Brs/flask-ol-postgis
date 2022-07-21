from celery import shared_task
import os 
import shutil

@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

import geopandas as gpd
from project.api.models import db, File, status_type
import os

@shared_task(bind=True)
def import_in_db(self):
    """
    todo: check File db (status based) and load shp into postgis
    """
    # add try excpet where except make the task be run another time
    shp_files = File.query.filter(File.status == status_type.UPLOADED, File.name.like('%.shp')).all()
    
    list_of_dir = [] #nasty way, since I also declare temp_path in views, I just wanted to test chain in celery
    
    for file in shp_files:

        list_of_dir.append(os.path.dirname(file.fp))

        shp_file = gpd.read_file(file.fp)
        dir_name = os.path.dirname(file.fp)
        #change column name in not-capitalized letters and name wihtout extension
        file_name_we = os.path.splitext(file.name)[0]
        try:
            shp_file.to_postgis(name=file_name_we,con=db.engine)

            file.status = status_type.SENT_TO_DB

            other_files = File.query.filter(File.status == status_type.UPLOADED, 
                                            File.name.notlike('%.shp'),
                                            File.fp.like(f"{dir_name}%")).all()
            
            for other_file in other_files:
                other_file.status = status_type.SENT_TO_DB
            
            db.session.commit()
        except Exception as exc:
            raise self.retry(
                exc=exc, 
                retry_kwargs={'max_retries': 7, 'countdown': 5}
            )
    return list_of_dir

@shared_task(bind=True)
def delete_file(self, paths):
    for path in paths:
        shutil.rmtree(path, ignore_errors=True)
    return "directory deleted"