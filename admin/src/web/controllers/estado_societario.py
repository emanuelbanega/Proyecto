from flask import Blueprint, render_template

from src.web.helpers.auth import token_required


estado_societario_blueprint = Blueprint(
    "estado_societario", __name__, url_prefix="/estado_societario"
)


@estado_societario_blueprint.get("/")
@token_required
def estado_societario():
    return render_template("estado_societario.html", nav_menu=False)
