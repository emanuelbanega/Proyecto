from src.core.quotas import quotaV2
from src.core.database import db
from src.core.associates.associated import Associated
from src.core.sports.sport import Sport
from datetime import datetime


def add_associated(**kwargs):
    # Agrega un asociado en la base de datos.
    associated = Associated(**kwargs)
    db.session.add(associated)
    db.session.commit()
    return associated


def delete_associated(associated):
    # Elimina un asociado en la base de datos.
    db.session.delete(associated)
    db.session.commit()
    return associated


def existing_associated(associated_document_number):
    # Devuelte True si existe un asociado con el mismo documento en la base de datos.
    return (
        Associated.query.filter_by(document_number=associated_document_number).first()
        is not None
    )


def find_associated_by_active(active, current_page, items):
    # Trae de la BD los asociados paginados con el estado = 'active'. Current_page es la pagina actual, items los elementos a mostrar.
    return (
        Associated.query.filter_by(condition=active)
        .order_by(Associated.id)
        .paginate(page=current_page, per_page=items)
    )


def find_associated_by_surname(surname, cant, current_page):
    return (
        Associated.query.filter_by(surname=surname)
        .order_by(Associated.id)
        .paginate(page=current_page, per_page=cant)
    )


def find_associated_by_surname_and_condition(surname, condition, cant, current_page):
    return (
        Associated.query.filter_by(surname=surname, condition=condition)
        .order_by(Associated.id)
        .paginate(page=current_page, per_page=cant)
    )


def get_associated_by_document_number(documentNum):
    """Retorna el asociado con numero de documento"""
    return Associated.query.filter_by(document_number=documentNum).first()


def list_active_associated():
    """Trae todos los asociados y filtra los no activos."""
    return Associated.query.filter_by(condition="Activo").all()


def list_associates_no_user(current_page, cant):
    """Trae todos los asociados (paginado) que no tienen usuario."""
    return (
        Associated.query.filter_by(user_id=None)
        .order_by(Associated.id)
        .paginate(page=current_page, per_page=cant)
    )


def change_status_associated(associated: Associated):
    """cambia el estado del asociado"""

    if associated.condition == "Activo":
        associated.condition = "No-activo"
    else:
        associated.condition = "Activo"

    db.session.commit()
    return associated


def list_signable_associated():
    """Trae todos los asociados activos, no morosos."""
    associates_ret = Associated.query.filter_by(condition="Activo").all()
    associates_filtered = []
    for a in associates_ret:
        if not is_defaulter(a.id):
            associates_filtered.append(a)
    return associates_filtered


def get_associated_by_id(id):
    # Busca y retorna un asociado por id.
    associated = Associated.query.get_or_404(id)
    return associated


def list_associated():
    # Trae todos los asociados de la base de datos.
    return Associated.query.all()


def list_associates_page(current_page, items):
    # Trae los asociados de la pagina idicada con el numero de items por pagina indicado.
    return Associated.query.order_by(Associated.id).paginate(
        page=current_page, per_page=items
    )


def get_signed_associated(sport, current_page, cant_elements):
    """Recibe una disciplina y retorna los asociados inscriptos."""
    result = Associated.query.filter(Associated.sports.contains(sport)).paginate(
        page=current_page, per_page=cant_elements
    )
    return result


def get_unsigned_associated(sport, current_page, cant_elements):
    """Recibe una disciplina y retorna los asociados no inscriptos."""
    result = Associated.query.filter(~Associated.sports.contains(sport)).paginate(
        page=current_page, per_page=cant_elements, error_out=False
    )
    return result


def remove_associate_user(associate):
    """Quita la relacion entre usuario y asociado."""
    associate.user_id = None
    db.session.commit()
    return associate


def verify_edit_associated(params):
    if not params["name"].replace(" ", "").isalpha():
        message = f"El nombre {params['name']} contiene caracteres no validos."
        return {"success": None, "message": message}

    if not params["surname"].replace(" ", "").isalpha():
        message = f"El apellido {params['surname']} contiene caracteres no validos."
        return {"success": None, "message": message}

    message = "Asociado editado correctamente"
    return {"success": True, "message": message}


def verify_new_associated(params):
    # Verificar que no sea repetida por nombre y division
    if existing_associated(params["document_number"]):
        message = f"El numero de documento {params['document_number']} pertenece a un asociado ya existente."
        return {"associated": None, "message": message}

    if not params["name"].replace(" ", "").isalpha():
        message = f"El nombre {params['name']} contiene caracteres no validos."
        return {"associated": None, "message": message}

    if not params["surname"].replace(" ", "").isalpha():
        message = f"El apellido {params['surname']} contiene caracteres no validos."
        return {"associated": None, "message": message}

    associated = add_associated(
        name=params["name"],
        surname=params["surname"],
        document_type=params["document_type"],
        document_number=params["document_number"],
        gender=params["gender"],
        direction=params["direction"],
        condition=params["condition"],
        phone=params["phone"],
        mail=params["mail"],
    )

    message = "Asociado creado correctamente"
    return {"associated": associated, "message": message}


def update_associated(associated):
    # Modifica el asociado con el dato enviado por parametro
    db.session.commit()
    return associated


def is_defaulter(associated_id):
    quotas = quotaV2.get_quotas_by_state_by_associated_id(associated_id, False)
    for q in quotas:
        if q.end_date < datetime.now():
            return True
    return False


def edit_profile_associated(associated: Associated, data):
    """Actualiza el perfil del asociado"""
    associated.name = data["first_name"].strip()
    associated.surname = data["last_name"].strip()
    associated.direction = data["address"].strip()
    if data["phone"]:
        associated.phone = str(data["phone"]).strip()
    else:
        associated.phone = None
    db.session.commit()
    return associated
