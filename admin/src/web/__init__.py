import logging
from os import getcwd

from flask import Flask, render_template
from flask_session import Session
from flask import session, redirect, url_for

from src.core import database
from src.core import seeds
from src.web.config import config
from src.web.helpers import handlers
from src.web.controllers.perfil import perfil_blueprint
from src.web.controllers.estado_societario import estado_societario_blueprint
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.users import user_blueprint
from web.controllers.sports import sport_blueprint
from web.controllers.associates import associated_blueprint
from web.controllers.config import config_blueprint
from web.controllers.signups import signup_blueprint
from web.controllers.payments import payment_blueprint
from web.controllers.quotas import quotas_blueprint
from web.controllers.api import api_blueprint
from src.web.helpers import auth, user

from flask_jwt_extended import JWTManager


# Descomenta estas lineas si quieres ver información en consola de la base
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(env="development", static_folder="static"):
    """Metodo de inicialización de la aplicación."""

    app = Flask(__name__, static_folder=static_folder)

    # Load config
    app.config.from_object(config[env])

    if env == "development":
        app.config["UPLOAD_FOLDER"] = app.static_folder

        from flask_cors import CORS

        # CORS
        cors = CORS(
            app,
            supports_credentials=True,
            resources={
                r"/api/*": {
                    "origins": [
                        "https://grupo17.proyecto2022.linti.unlp.edu.ar",
                        "http://127.0.0.1:5173",
                        "http://localhost:5173",
                    ]
                }
            },
        )
    else:
        app.config["UPLOAD_FOLDER"] = getcwd() + "/public"

    # Init database
    database.init_app(app)

    # Config session backend
    Session(app)

    # JWT
    jwt = JWTManager(app)

    @app.get("/")
    def home():
        if not auth.is_authenticated(session):
            return redirect(url_for("auth.login"))
        return render_template("home.html")

    # rutas de la app
    app.register_blueprint(perfil_blueprint)
    app.register_blueprint(estado_societario_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(config_blueprint)
    app.register_blueprint(sport_blueprint)
    app.register_blueprint(associated_blueprint)
    app.register_blueprint(signup_blueprint)
    app.register_blueprint(payment_blueprint)
    app.register_blueprint(quotas_blueprint)
    app.register_blueprint(api_blueprint)

    # manejo de errores
    app.register_error_handler(401, handlers.unauthorized)
    app.register_error_handler(403, handlers.forbidden)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(405, handlers.Method_Not_Allowed)
    app.register_error_handler(500, handlers.internal_server_error)

    # Jinja
    app.jinja_env.globals.update(email_has_permission=auth.email_has_permission)
    app.jinja_env.globals.update(user_is_role=user.user_is_role)

    # comando para resetear la base
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    # comando para setear la base con algunas tablas ya hechas
    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()

    return app
