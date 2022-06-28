from celery import Celery, current_app as current_celery_app
import os


def make_celery(app):
    #celery = current_celery_app
    #celery.config_from_object(app.config, namespace="CELERY")
    #celery.config_from_object(app.config)
    celery = Celery(app.import_name, broker="redis://redis:6379/0", backend="redis://redis:6379/0",) #todo get env var
    celery.conf.update(app.config)
    return celery