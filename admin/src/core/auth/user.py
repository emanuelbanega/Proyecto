from datetime import datetime

from string import punctuation

from src.core.database import db
from src.core.auth.role import rol_tiene_permiso

users_roles = db.Table(
    "users_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("Users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)


class User(db.Model):

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    photo = db.Column(db.String(100), nullable=False, default="sin-usuario.png")
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(150), nullable=False, default="-")
    role = db.relationship("Role", secondary=users_roles)
    associated = db.relationship("Associated", back_populates="user")
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


def existing_mail(email):
    """Devuelve True si existe en email en la BD"""
    return User.query.filter_by(email=email).first() is not None


def existing_userName(userName):
    """Devuelve True si existe el userName en la BD"""
    return User.query.filter_by(userName=userName).first() is not None


def user_tiene_permiso(user, namePermission):
    """Recorre los permisos del usuario, devuelve True si encuentra 'namePermission'"""

    for role in user.role:
        if rol_tiene_permiso(role, namePermission):
            return True
    return False


def verfy_name_user(userName):
    # userName sin espacios
    if " " in userName.strip():
        message = "El nombre de Usuario no debe contener espacios"
        return {"result": False, "message": message}


def asig_associate(user, associ):
    """asigna un asociado a un usuario y lo actualiza en la BD"""
    user.associated.append(associ)
    associ.mail = user.email
    db.session.add(associ)
    db.session.add(user)
    db.session.commit()
