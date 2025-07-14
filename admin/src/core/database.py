from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def init_app(app):
    db.init_app(app)
    bcrypt.init_app(app)
    config_db(app)


def config_db(app):
    # ojo, esto crea todas las tablas de la base de datos
    @app.before_first_request
    def init_database():
        db.create_all()

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()


def reset_db():
    print(" Eliminando base de datos...")
    db.drop_all()
    print(" Creando base de datos...")
    db.create_all()
    print(" Done!")
