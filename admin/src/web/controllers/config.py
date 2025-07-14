from calendar import c
from src.web.helpers.auth import token_required, decode_token
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from src.core import setting
from src.core import auth

config_blueprint = Blueprint("config", __name__, url_prefix="/config")


@config_blueprint.get("/")
@token_required
def config():
    userToken = decode_token(session.get("user"))
    if userToken is None:
        return redirect(url_for("auth.logout"))
    user = auth.find_user_by_mail(userToken["user"])
    user_can_update = auth.user_has_role(user.items[0], "administrador")
    conf = setting.get_setting()
    return render_template(
        "config.html",
        nav_menu=False,
        settingObj=conf,
        user_can_update=user_can_update,
        currency_types=setting.get_currency_types(),
    )


@config_blueprint.post("/")
def save_config():
    """Actualiza los valores de la configuracion y redirecciona."""
    aux = setting.get_setting()
    params = request.form
    result = setting.verify_edit_config(params)

    if not result["success"]:
        flash(result["message"], "error")
        return redirect(url_for("config.config"))

    aux.cant_elements_page = params["cantElements"]
    value = params["enablePayTable"]
    if value == "1":
        aux.enable_pay_table = True
    else:
        aux.enable_pay_table = False
    aux.contact_info = params["contactInfo"]
    aux.voucher_title = params["voucherTitle"]
    aux.price_month = params["priceMonth"]
    aux.percent_increase_debtors = params["percentIncrease"]
    aux.currency_type = params["currencyType"]
    aux.description_home = params["descriptionHome"]
    aux.contact_email = params["contactEmail"]
    setting.update_setting(aux)

    flash(result["message"], "success")
    return redirect(url_for("config.config"))
