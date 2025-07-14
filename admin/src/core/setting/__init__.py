from string import punctuation
from src.core.database import db
from src.core.setting.setting import Setting
from src.web.helpers.validate import email


def create_setting(**kwargs):
    """agrega la configuracion de la app a la BD. recibe 'cant_elements_page', 'enable_pay_table', 'contact_info', 'voucher_title', 'price_month', 'percent_increase_debtors', 'currency_type'."""
    setting = Setting(**kwargs)
    db.session.add(setting)
    db.session.commit()

    return setting


def update_setting(setting):
    """Actualiza la configuracion con la enviada por parametro."""
    db.session.commit()
    return setting


def get_setting():
    """Trae la configuracion de la App."""
    array = Setting.query.all()
    return array[0]


def verify_edit_config(params):
    """Verifica los datos de la configuracion para editar."""
    result = verify_config(params)
    if not result["success"]:
        return result

    message = "Configuracion actualizada correctamente"
    return {"success": True, "message": message}


def verify_config(params):
    """Verifica los datos de la configuracion nueva."""

    if not int(params["cantElements"]) > 0:
        message = "La cantidad de elementos de pagina debe ser mayor a 0"
        return {"success": False, "message": message}

    if not float(params["priceMonth"]) > 0:
        message = "El valor mensual debe ser mayor a 0"
        return {"success": False, "message": message}

    if not float(params["percentIncrease"]) > 0:
        message = "El porcentaje de deuda debe ser mayor a 0"
        return {"success": False, "message": message}

    if len(params["descriptionHome"]) > 300:
        message = "La descripción del home no puede tener más de 300 caracteres"
        return {"success": False, "message": message}

    if any(
        [
            True if c in punctuation and not c in "-_.%°/!¡?¿" else False
            for c in params["descriptionHome"]
        ]
    ):
        message = "La descripción solo acepta estos caracteres especiales: '-', '_', '.', '%', '°', '/', '!', '¡', '?', '¿'"
        return {"success": False, "message": message}

    if not email(params["contactEmail"]):
        message = "El email no es valido o supera los 50 caracteres"
        return {"success": False, "message": message}

    return {"success": True, "message": None}


def get_currency_types():
    return ("ARS", "USD", "EUR", "MXN")
