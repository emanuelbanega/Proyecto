from src.core.database import db
from src.core.sports.sport import Sport


def list_sports():
    """Trae todas las disciplinas de la BD."""
    return Sport.query.all()


def list_enabled_sports():
    """Trae todas las disciplinas activas."""
    return Sport.query.filter_by(enabled=True)


def list_sports_page(current_page, items):
    """Trae las diciplinas de la pagina idicada con el numero de items por pagina indicado."""
    return Sport.query.order_by(Sport.id).paginate(page=current_page, per_page=items)


def list_sports_page_filtered(current_page, items, value, name):
    """Trae disciplinas filtradas, paginadas."""
    if value is not None and name is not None:
        return (
            Sport.query.order_by(Sport.id)
            .filter_by(enabled=value, name=name)
            .paginate(page=current_page, per_page=items)
        )
    elif value is not None:
        return (
            Sport.query.order_by(Sport.id)
            .filter_by(enabled=value)
            .paginate(page=current_page, per_page=items)
        )
    elif name is not None:
        return (
            Sport.query.order_by(Sport.id)
            .filter_by(name=name)
            .paginate(page=current_page, per_page=items)
        )
    else:
        return Sport.query.order_by(Sport.id).paginate(
            page=current_page, per_page=items
        )


def get_sport_by_id(id):
    """Busca y trae una disciplina por ID."""
    sport = Sport.query.get_or_404(id)
    return sport


def get_sport_by_id_no_404(id):
    """Busca y trae una disciplina por ID, no 404."""
    sport = Sport.query.filter_by(id=id).first()
    return sport


def delete_sport(sport):
    """Elimina una disciplina de la BD."""
    db.session.delete(sport)
    db.session.commit()
    return sport


def add_sport(**kwargs):
    """Crea una disciplina nueva en la DB."""
    sport = Sport(**kwargs)
    db.session.add(sport)
    db.session.commit()
    return sport


def update_sport(sport):
    """Actualiza la disciplina con la enviada por parametro."""
    db.session.commit()
    return sport


def append_to_associates(sport, associate):
    """Agrega un asociado a la disciplina."""
    sport.associates.append(associate)
    db.session.commit()
    return sport


def filter_signable(sport, associates):
    """Devuelve los asociados no inscriptos en la disciplina."""
    # Obtiene ids de los inscriptos en la discipilina.
    signed_ids = [each.id for each in sport.associates]
    # Filtra los asociados cuyas ids se encuentren en signed_ids.
    filtered = [each for each in associates if each.id not in signed_ids]
    return filtered


def delete_singup(sport, associate):
    """Elimina una inscripcion."""
    sport.associates.remove(associate)
    update_sport(sport)
    return


def verify_sport(params):
    """Verifica los datos de la disciplina."""
    # Verifica que el nombre de la disciplina no contenga caracteres que no sean letras
    if not params["sportName"].replace(" ", "").isalpha():
        message = "Nombre contiene caracteres no validos"
        return {"success": False, "message": message}

    # Verificar que la division no contenga caracteres invalidos
    if not ((params["division"].replace(" ", "").replace("-", "")).isalnum()):
        message = "Division contiene caracteres no validos"
        return {"success": False, "message": message}

    # Verificar que los nombres de instructores solo contengan letras
    if not (params["instructors"].replace(" ", "").replace(",", "")).isalpha():
        message = "Instructores no es una lista de nombres validos"
        return {"success": False, "message": message}

    # Verificar que los horarios sean validos
    if not (
        params["schedule"].replace(" ", "").replace(",", "").replace(":", "")
    ).isalnum():
        message = "Horarios no es una lista de horarios validos"
        return {"success": False, "message": message}

    # Verificar que la cuota sea un numero
    if not params["fee"].replace(".", "").isdigit():
        message = "Valor de cuota invalido, tenga en cuenta no es necesario agregar el signo $ y solo se aceptan numeros enteros."
        return {"success": False, "message": message}

    return {"success": True, "message": None}


def verify_sport_len(params):
    """Verifica el tamaño de los datos para una disciplina."""

    if len(params["sportName"]) > 50:
        message = "Nombre maximo 50 caracteres."
        return {"success": False, "message": message}

    if len(params["division"]) > 50:
        message = "Division maximo 50 caracteres."
        return {"success": False, "message": message}

    if len(params["instructors"]) > 300:
        message = "Instructores maximo 300 caracteres."
        return {"success": False, "message": message}

    if len(params["schedule"]) > 300:
        message = "Horarios maximo 300 caracteres."
        return {"success": False, "message": message}

    if len(params["fee"]) > 10:
        message = "Cuota maximo 10 cifras."
        return {"success": False, "message": message}

    return {"success": True, "message": None}


def existing_sport(sport_name, division_name):
    """Devuelte True si existe la combinacion de nombre y division en la BD."""
    return (
        Sport.query.filter_by(name=sport_name, division=division_name).first()
        is not None
    )


def verify_new_sport(params, enable):
    """Verifica los datos para una disciplina nueva."""
    result = verify_sport(params)
    if not result["success"]:
        return {"sport": None, "message": result["message"]}

    result = verify_sport_len(params)
    if not result["success"]:
        return {"sport": None, "message": result["message"]}

    # Verificar que no sea repetida por nombre y division
    if existing_sport(params["sportName"], params["division"]):
        message = "Disciplina existente"
        return {"sport": None, "message": message}

    sport = add_sport(
        name=params["sportName"],
        division=params["division"],
        instructors_names=params["instructors"],
        schedule=params["schedule"],
        monthly_fee=params["fee"].replace(".", ""),
        enabled=enable,
    )

    message = "Disciplina creada correctamente"
    return {"sport": sport, "message": message}


def verify_edit_sport(params, sport):
    """Verifica los datos de la disciplina a editar."""
    result = verify_sport(params)
    if not result["success"]:
        # return {"sport": None, "message": result["message"]}
        return result

    result = verify_sport_len(params)
    if not result["success"]:
        # return {"sport": None, "message": result["message"]}
        return result

    # Verificar que, o que el nuevo nombre/division no existen ya, o que no se hayan cambiado
    if not (params["sportName"] == sport.name and params["division"] == sport.division):
        if existing_sport(params["sportName"], params["division"]):
            message = "Disciplina existente"
            # return {"sport": None, "message": message}
            return {"success": False, "message": message}

    message = "Disciplina editada correctamente"
    return {"success": True, "message": message}


def delete_all_signed(sport):
    """Elimina todos los inscriptos de la disciplina."""
    sport.associates.clear()
    return sport


def invert_sport_enabled(sport):
    """Invierte el valor de enabled en la disciplinas."""
    if sport.enabled:
        sport.enabled = False
    else:
        sport.enabled = True

    return sport
