import os


basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = set(['shp', 'shx', 'prj', 'dbf'])