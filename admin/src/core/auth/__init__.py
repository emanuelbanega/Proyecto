import re
import os
import base64

from random import sample

from flask import current_app

from src.core.database import db, bcrypt
from src.core.auth.user import (
    User,
    existing_mail,
    existing_userName,
    user_tiene_permiso,
    asig_associate,
)
from src.core.auth.role import Role
from src.core.auth.permission import Permission


def list_Users():
    """Trae todos los usuarios de la BD"""
    return User.query.all()


def list_Users_paginate(current_page, items):
    """Trae todos los usuarios de la BD paginados, items es la cantidad de elementos a mostrar, current_page la pagina que devuelve"""
    return User.query.order_by(User.id).paginate(
        page=current_page, per_page=items, error_out=False
    )


def create_User(**kwargs):
    """agrega un nuevo usuario a la BD. recibe 'email', 'userName', 'password', 'active', 'first_name', 'last_name'"""
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def delete_by_id(user_id):
    """"""
    user = find_user_by_id(user_id)
    for rol in user.role:
        if rol.name == "administrador":
            message = "No se puede eliminar un usuario administrador"
            return {"user": None, "message": message}
        if rol.name == "socio":
            for associate in user.associates:
                if associate.condition == "Activo":
                    message = "No se puede eliminar un socio con asociado activo"
                    return {"user": None, "message": message}

    db.session.delete(user)
    db.session.commit()
    message = "Usuario eliminado"
    return {"user": user, "message": message}


def block_user(user_id):
    """Verifica que el usuario no tenga rol administrador y lo bloquea"""
    user = find_user_by_id(user_id)
    for rol in user.role:
        if rol.name == "administrador":
            message = "No se puede bloquear a un usuario administrador"
            return {"user": None, "message": message}
    user.active = not user.active

    db.session.commit()
    message = "Estado actualizado"
    return {"user": user, "message": message}


def verify_new_user(params):
    """Verifica que los datos del nuevo usuario"""

    if existing_mail(params["email"].lower().strip()):
        message = "Correo existente"
        return {"user": None, "message": message}

    if existing_userName(params["userName"].strip()):
        message = "Nombre de usuario existente"
        return {"user": None, "message": message}

    passHash = bcrypt.generate_password_hash(params["password"]).decode("utf-8")
    user = create_User(
        email=params["email"].lower().strip(),
        userName=params["userName"].strip(),
        password=passHash,
        first_name=params["first_name"].strip(),
        last_name=params["last_name"].strip(),
    )
    message = "Usuario agregado correctamente"
    return {"user": user, "message": message}


def verify_update_user(params, user):
    """Verifica que los datos del usuario actualizado"""
    passHash = None
    if params["password"] != params["confirmacion"]:
        message = "Las contraseñas no coinciden"
        return {"user": None, "message": message}

    nameUserExist = User.query.filter_by(userName=params["userName"].strip()).first()
    if nameUserExist is not None:
        if nameUserExist.id != user.id:
            message = "Nombre de usuario existente"
            return {"user": None, "message": message}

    if params["password"] != "":
        passHash = bcrypt.generate_password_hash(params["password"]).decode("utf-8")
        user.password = passHash

    user.userName = params["userName"].strip()
    user.first_name = params["first_name"]
    user.last_name = params["last_name"]
    db.session.commit()
    message = "Usuario actualizado"
    return {"user": user, "message": message}


def list_Roles():
    """Trae todos los roles de la BD"""
    return Role.query.all()


def create_Role(**kwargs):
    """agrega un nuevo rol en la BD. recibe 'name'"""
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


def assign_role(user, role):
    """asigna un rol a un usuario y lo guarda en la BD"""
    user.role.append(role)
    db.session.add(user)
    db.session.commit()

    return user


def remove_user_role(user, role):
    """Quita el rol al usuario"""
    user.role.remove(role)
    db.session.add(user)
    db.session.commit()

    return user


def create_Permission(**kwargs):
    """agrega un nuevo permiso en la BD. recibe 'name'"""
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission


def assign_permission(permission, role):
    """asigna un permiso a un rol y lo guarda en la BD"""
    role.permission.append(permission)
    db.session.add(role)
    db.session.commit()

    return role


def find_role_by_name(name):
    """Busca en la BD el rol con nombre 'name'"""
    return Role.query.filter_by(name=name).first()


def find_user_by_mail_pass(email, password):
    """Devuelve un usuario segun su email y pass"""
    user = User.query.filter_by(email=email.lower().strip()).first()
    if not user:
        return user
    if bcrypt.check_password_hash(user.password, password):
        return user

    return None


def convert_to_binary(photo):
    """Convierte una foto a binario"""
    with open(photo, "rb") as f:
        blob = f.read()

    return blob


def convert_to_base64(photo):
    with open(photo, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


def save_base64_user(file_content, userEmail):
    newNameFile = stringRandom() + ".jpg"
    try:
        file_content = base64.b64decode(file_content)
        path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], "images/users", newNameFile
        )

        with open(path, "wb") as f:
            f.write(file_content)
            f.close()
    except Exception as e:
        print("error:", str(e))
    else:
        change_user_photo(userEmail, newNameFile)


def change_user_photo(userEmail, nameImg):
    """Actualiza el nombre de la imagen de usuario"""
    user = User.query.filter_by(email=userEmail).first()
    if user.photo != "sin-usuario.png":

        # Elimina la foto anterior si el usuario no tiene asociado, no tiene credencial y la foto del carnet es distinta a la de usuario
        if not (
            user.associated
            and user.associated[0].credential
            and user.associated[0].credential[0].photo == user.photo
        ):
            photo_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], "images/users", user.photo
            )
            os.remove(photo_path)
    user.photo = nameImg

    db.session.commit()
    return user


def stringRandom():
    """Genera un string aleatorio"""
    string_random = "0123456789abcdefghijkmnopqrstuvwxyz_"
    long = 20
    sequence = string_random.upper()
    result_random = sample(sequence, long)
    string_random = "".join(result_random)
    return string_random


def save_photo_user(extension, file, userEmail):
    """crea un nuevo nombre y guarda la foto en la ruta por defecto"""
    # asigno un nombre nuevo random, para evitar coincidencias
    newNameFile = stringRandom() + extension
    try:

        # establezco la ruta para guardar y lo guardo
        upload_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], "images/users", newNameFile
        )
        file.save(upload_path)
        file.close()
    except Exception as e:
        print("error:", str(e))
    else:
        # actualizo la foto del usuario
        change_user_photo(userEmail, newNameFile)
        return newNameFile


def edit_description_user(user: User, des: str):
    """Actualiza la descripcíon del usuario"""
    user.description = des

    db.session.commit()
    return user


def edit_profile_user(user: User, data):
    """Actualiza el perfil del usuario"""

    user.first_name = data["first_name"].strip()
    user.last_name = data["last_name"].strip()
    user.userName = data["user"].strip()
    if data["description"]:
        user.description = data["description"].strip()
    else:
        user.description = "-"
    db.session.commit()
    return user


def find_user_by_mail(email):
    """Devuelve un usuario segun su email. Lo devuelve PAGINADO"""
    return User.query.filter_by(email=email.lower().strip()).paginate(1, 1)


def find_user_by_active(active, current_page, items):
    """Trae de la BD los usuarios paginados con el estado= 'active'. Current_page es la pagina actual, items los elementos a mostrar"""
    return (
        User.query.filter_by(active=active)
        .order_by(User.id)
        .paginate(page=current_page, per_page=items, error_out=False)
    )


def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


def email_tiene_permisos(email_user, permission):
    user = User.query.filter_by(email=email_user.lower().strip()).first()
    return user_tiene_permiso(user, permission)


def user_has_role(user, nameRole):
    for role in user.role:
        if role.name == nameRole:
            return True
    return False


def verify_asig_associate(user, associate):
    """Verifica que el asociado no tenga un socio asignado y luego los relaciona"""
    if user.associated:
        message = "El usuario ya tiene asociado asignado"
        return {"user": None, "message": message}
    if associate.user_id is not None:
        message = "El asociado ya tiene una cuenta Socio vinculada"
        return {"user": None, "message": message}
    asig_associate(user, associate)
    message = "Usuario actualizado"
    return {"user": user, "message": message}
