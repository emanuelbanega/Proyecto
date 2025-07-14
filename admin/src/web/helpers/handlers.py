from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not found Error",
        "error_description": "La url a la que quieres acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized(e):
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": "Debe iniciar sesión para acceder al recurso",
    }
    return render_template("error.html", **kwargs), 401


def forbidden(e):
    kwargs = {
        "error_name": "403 Forbidden",
        "error_description": "No posees los permisos necesarios para esta acción.",
    }
    return render_template("error.html", **kwargs), 403


def Method_Not_Allowed(e):
    kwargs = {
        "error_name": "405 Method Not Allowed",
        "error_description": "No tienes permitido realizar esta acción atreves de la URL",
    }
    return render_template("error.html", **kwargs), 405


def internal_server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Error interno del servidor",
    }
    return render_template("error.html", **kwargs), 500
