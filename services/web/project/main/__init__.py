from flask import Blueprint

main_blueprint = Blueprint("main", __name__, url_prefix="/main", template_folder="templates")

from . import views