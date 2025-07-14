import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import session, abort, flash, redirect, url_for, current_app

from src.core.auth import email_tiene_permisos


def is_authenticated(session):
    return session.get("user") != None


def email_has_permission(userToken, permiso):
    email_user = decode_token(userToken)["user"]
    return email_tiene_permisos(email_user, permiso)


def user_has_permission(permiso):
    """Corrobora que el usuario tenga el permiso"""

    def probandoDeco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            email_user = decode_token(session.get("user"))["user"]
            if not email_tiene_permisos(email_user, permiso):
                return abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return probandoDeco


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # me falta ver como traer la secret_key
        if session.get("user") is None:
            return abort(401)
        token = decode_token(session.get("user"))
        if not token:
            del session["user"]
            del session["name"]
            del session["photo"]
            session.clear()
            return abort(401)
        if token["expiration"] < str(datetime.utcnow()):
            del session["user"]
            del session["name"]
            del session["photo"]
            session.clear()
            flash("La sesión ha expirado.", "error")
            return redirect(url_for("auth.login"))
        session["user"] = generate_token(token["user"])
        return f(*args, **kwargs)

    return decorated_function


def generate_token(user):
    """Genera un token con email de user, y una expiración de 2hs"""
    # falta traer la secret_key
    return jwt.encode(
        {
            "user": user,
            "expiration": str(datetime.utcnow() + timedelta(hours=2)),
        },
        current_app.secret_key,
    )


def decode_token(token):
    """decodifica la clave token"""
    # falta traer la secret_key
    try:
        return jwt.decode(
            token,
            current_app.secret_key,
            algorithms=["HS256"],
        )
    except:
        return None
