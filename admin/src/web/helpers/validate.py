import re
from string import punctuation


def email(email):
    """Verifica que el email sea valido"""
    if len(email) > 50:
        return False
    reglaEmail = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(reglaEmail, email.lower().strip()) is not None


def userName(name):
    """Verifica que el userName sea correcto"""
    if len(name) > 50:
        return False
    if " " in name.strip():
        return False
    if any([True if c in punctuation and not c in "-_" else False for c in name]):
        return False
    return True


def name(newName):
    """Verifica que el nombre sea correcto"""
    # name sin numeros, ni signos
    if len(newName) > 40:
        return False
    return not (
        any([c.isdigit() for c in newName])
        or any([True if c in punctuation else False for c in newName])
    )


def description(newDescription):
    """Verifica que la descripción sea correcto"""
    if len(newDescription) > 150:
        return False
    if any(
        [True if c in punctuation and not c in "-_." else False for c in newDescription]
    ):
        return False
    return True


def address(newAddress):
    """Verifica que la dirección sea correcto"""
    if len(newAddress) > 30:
        return False
    if any([True if c in punctuation and not c in "°" else False for c in newAddress]):
        return False
    return True


def phone(newPhone):
    """Verifica que la dirección sea correcto"""
    if len(newPhone) > 15:
        return False
    if any([True if c in punctuation and not c in "()-" else False for c in newPhone]):
        return False
    return True


def validatePassword(password):
    """Verifica password sea correcto"""
    # password mayor a 6 y menor a 20
    if len(password) < 6 or len(password) > 20:
        message = "La contraseña debe tener entre 6 y 20 caracteres."
        return {"user": None, "message": message}

    # password que contenga 1 numero
    if not any([c.isdigit() for c in password]):
        message = "La contraseña debe tener al menos 1 número"
        return {"user": None, "message": message}

    # password que tenga 1 minuscula
    if not any([c.islower() for c in password]):
        message = "La contraseña debe tener al menos una minúscula"
        return {"user": None, "message": message}

    # password que tenga 1 Mayuscula
    if not any([c.isupper() for c in password]):
        message = "La contraseña debe tener al menos una mayuscula"
        return {"user": None, "message": message}
    return {"user": True}


def validateProfileUser(data):
    if not name(data["first_name"].strip()):
        return {"Valid": False, "message": "Nombre no válido"}
    if not name(data["last_name"].strip()):
        return {"Valid": False, "message": "Apellido no válido"}
    if not userName(data["user"].strip()):
        return {"Valid": False, "message": "Nombre de usuario no válido"}
    if not description(data["description"].strip()):
        return {"Valid": False, "message": "Descripción no válida"}
    return {"Valid": True, "message": "Todo correcto"}


def validateProfileAssociated(data):
    if not name(data["first_name"].strip()):
        return {"Valid": False, "message": "Nombre no válido"}
    if not name(data["last_name"].strip()):
        return {"Valid": False, "message": "Apellido no válido"}
    if not address(data["address"].strip()):
        return {"Valid": False, "message": "Dirección no válida"}
    if data["phone"]:
        if not phone(str(data["phone"]).strip()):
            return {"Valid": False, "message": "Número de teléfono válido"}
    return {"Valid": True, "message": "Todo correcto"}
