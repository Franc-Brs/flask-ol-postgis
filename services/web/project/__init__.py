import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from project.config import config
from flask_log_request_id import RequestID

from flask_celeryext import FlaskCeleryExt
from project.celery_utils import make_celery

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ext_celery.init_app(app)

    RequestID(app)
    
    # new
    # register blueprint
    from project.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from project.main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/application")


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app