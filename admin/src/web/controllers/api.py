import re
import os

from datetime import datetime
from dateutils import relativedelta

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from flask_jwt_extended import get_jwt_identity, get_csrf_token
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)

from src.core import sports
from src.core import associates
from src.core import payments
from src.core import auth
from src.core import setting
from src.core import quotas
from src.core import licenses
from src.web.helpers.auth import generate_token, decode_token
from src.web.helpers import validate
from src.core.quotas.quotaV2 import (
    QuotaJson,
    get_quota_by_id,
    assign_payment,
    get_detail_quota,
)
from src.core.quotas.quotaV2 import get_quotas_by_state_by_associated_id
from src.web.helpers.chart import array_last_months

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.get("/club/sports")
def return_sports_json():
    """Devuelve el listado de disciplians en formato json."""
    sports_ret = sports.list_enabled_sports()
    sports_json = []
    for sport in sports_ret:
        associates_names = []
        for each in sport.associates:
            associates_names.append(
                {
                    "Name": each.name,
                    "Surname": each.surname,
                }
            )
        sports_json.append(
            {
                "id": sport.id,
                "Name": sport.name + " " + sport.division,
                "Schedule": sport.schedule,
                "Teachers": sport.instructors_names,
                "Fee": sport.monthly_fee + " " + setting.get_setting().currency_type,
                "Signedup": associates_names,
            }
        )

    return sports_json


@api_blueprint.get("/me/sports")
@jwt_required()
def return_my_sports_json():
    """Devuelve las disciplinas del asociado en formato json."""
    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]
    role = auth.find_role_by_name("socio")

    # Verificar que el usuario posee rol socio
    if role not in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )

    # Verificar que el usuario posee un asociado
    if not user.associated[0]:
        return (
            jsonify({"msg": "No se encontró ningún asociado"}),
            404,
        )
    associated = user.associated[0]

    associated_sports = associated.sports
    sports_json = []

    for sport in associated_sports:
        associates_names = []
        for each in sport.associates:
            associates_names.append(
                {
                    "Name": each.name,
                    "Surname": each.surname,
                }
            )
        sports_json.append(
            {
                "id": sport.id,
                "Name": sport.name + " " + sport.division,
                "Schedule": sport.schedule,
                "Teachers": sport.instructors_names,
                "Fee": sport.monthly_fee + " " + setting.get_setting().currency_type,
                "Signedup": associates_names,
            }
        )

    return sports_json


@api_blueprint.get("/sport/<int:num>")
def get_sport(num):
    """Retorna la informacion de una disciplina especifica."""
    # sport_id = request.headers.get("sport_id")
    sport_id = num

    # Verificar que se haya incluido un id
    # if not sport_id:
    #    return jsonify({"msg": "Falta la id de la disciplina"}), 404

    # Verificar que id sea un numero
    # if not sport_id.isdigit():
    #    return jsonify({"msg": "Id no es un numero"}), 404

    sport = sports.get_sport_by_id_no_404(sport_id)

    # Verificar que id corresponda a una disciplina
    if not sport:
        return jsonify({"msg": "Id no es una disciplina valida"}), 404

    return jsonify(
        {
            "name": sport.name,
            "division": sport.division,
            "instructors": sport.instructors_names,
            "schedule": sport.schedule,
            "monthly_fee": sport.monthly_fee,
        }
    )


@api_blueprint.get("/sport/signedup/<int:num>")
def get_sport_signedup(num):
    """Retorna los inscriptos a una disciplinas especifica."""
    # sport_id = request.headers.get("sport_id")
    sport_id = num

    # Verificar que se haya incluido un id
    # if not sport_id:
    #     return jsonify({"msg": "Falta la id de la disciplina"}), 404

    # Verificar que id sea un numero
    # if not sport_id.isdigit():
    #     return jsonify({"msg": "Id no es un numero"}), 404

    sport = sports.get_sport_by_id_no_404(sport_id)

    # Verificar que id corresponda a una disciplina
    if not sport:
        return jsonify({"msg": "Id no es una disciplina valida"}), 404

    associates_ret = []
    for each in sport.associates:
        associates_ret.append(
            {
                "name": each.name,
                "surname": each.surname,
                "gender": each.gender,
            }
        )

    return jsonify(associates_ret)


@api_blueprint.get("/me/payments")
@jwt_required()
def get_my_payments():
    """Retorna los pagos de un asociado"""
    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]
    role = auth.find_role_by_name("socio")

    # Verificar que el usuario posee rol socio
    if role not in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )

    # Verificar que el usuario posee un asociado
    if not user.associated[0]:
        return (
            jsonify({"msg": "No se encontró ningún asociado"}),
            404,
        )

    associated_id = user.associated[0].id

    payments_list = payments.find_payment_by_id_associated(int(associated_id))
    payments_json = []
    for p in payments_list:
        payments_json.append({"date": p.date, "amount": p.amount, "state": p.state})
    return payments_json


@api_blueprint.get("/me/quotas")
@jwt_required()
def get_my_quotas():
    """Retorna las quotas de un asociado"""
    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]
    role = auth.find_role_by_name("socio")

    # Verificar que el usuario posee rol socio
    if role not in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )

    # Verificar que el usuario posee un asociado
    if not user.associated[0]:
        return (
            jsonify({"msg": "No se encontró ningún asociado"}),
            404,
        )

    associated_id = user.associated[0].id

    quotas_list = get_quotas_by_state_by_associated_id(associated_id, False)

    quotas_json = []

    amount_extra = 0

    if associates.is_defaulter(associated_id):
        amount_extra += setting.get_setting().percent_increase_debtors

    for q in quotas_list:
        quota_parsed = QuotaJson.fromJSON(q.dataJSON)
        quotas_json.append(
            {
                "id": q.id,
                "end_date": q.end_date,
                "amount": quota_parsed.total_amount + amount_extra,
                "currency_type": quota_parsed.currency_type,
            }
        )

    return quotas_json


@api_blueprint.post("/me/payments")
@jwt_required()
def add_payment():
    """Agrega un nuevo pago"""
    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]
    role = auth.find_role_by_name("socio")

    # Verificar que el usuario posee rol socio
    if role not in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )

    # Verificar que el usuario posee un asociado
    if not user.associated[0]:
        return (
            jsonify({"msg": "No se encontró ningún asociado"}),
            404,
        )

    associated_id = user.associated[0].id

    data = request.json
    quota_id = data["quota_id"]

    quota = get_quota_by_id(int(quota_id))

    if quota.state:
        return {"result": "error", "msg": "La cuota ya se encuentra paga"}, 400

    if not data["voucher_image"]:
        return jsonify({"msg": "No se mando ningun archivo"}), 400

    total_amount = QuotaJson.fromJSON(quota.dataJSON).total_amount

    if associates.is_defaulter(associated_id):
        total_amount += setting.get_setting().percent_increase_debtors


    payment = payments.add_payment(
        orden=quota.id + 1000, amount=total_amount, state=False
    )

    assign_payment(quota, payment)

    payments.save_base64_payment(data["voucher_image"], data["ext"], payment)

    return {"result": "success", "msg": "Se registro informacion del pago"}, 200


# segunda entrega
@api_blueprint.post("/auth")
def auth_token():
    """Inicio de sesion atravez de la api, devuelve un token por cookies"""
    data = request.get_json()
    # regla para correo valido
    reglaEmail = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if not re.match(reglaEmail, data["user"].lower().strip()) is not None:
        return (
            jsonify({"msg": "Correo no válido"}),
            404,
        )

    user = auth.find_user_by_mail_pass(data["user"], data["password"])
    if not user:
        return (
            jsonify({"msg": "Email o contraseña incorrecta."}),
            403,
        )
    if not user.active:
        return (
            jsonify({"msg": "Usuario bloqueado."}),
            401,
        )
    role = auth.find_role_by_name("socio")
    if not role in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )
    access_token = create_access_token(identity=user.email)
    response = jsonify()
    set_access_cookies(response, access_token)
    return response, 201


@api_blueprint.get("/logout")
@jwt_required()
def logout_jwt():
    """Cierra la sesion desaciendo la cookie"""
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


@api_blueprint.get("/me/profile")
@jwt_required()
def get_my_profile():
    """Devuelve el perfil del usuario"""

    current_user = get_jwt_identity()
    user = auth.find_user_by_mail(current_user).items[0]
    role = auth.find_role_by_name("socio")
    if not role in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )

    photo = (
        "https://admin-grupo17.proyecto2022.linti.unlp.edu.ar/public/images/users/"
        + user.photo
    )

    if not user.associated[0]:
        return (
            jsonify({"msg": "No se encontró ningún asociado"}),
            404,
        )
    associated = user.associated[0]
    if len(associated.credential) != 0:
        respuesta = "Con carnet"
    else:
        respuesta = "Sin carnet"
    return (
        jsonify(
            {
                "user": user.userName,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "photo": photo,
                "description": user.description,
                "number": str(associated.id),
                "document_type": associated.document_type,
                "document_number": associated.document_number,
                "gender": associated.gender,
                "address": associated.direction,
                "phone": associated.phone,
                "has_credential": respuesta
            }
        ),
        200,
    )


@api_blueprint.post("/me/profile")
@jwt_required()
def act_profile():
    """Actualiza el perfil del usuario"""

    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]

    data = request.get_json()
    if not data:
        return jsonify({"msg": "No se recibio los nuevos datos"}), 400
    result = validate.validateProfileUser(data)
    if not result["Valid"]:
        return jsonify({"msg": result["message"]}), 400
    result = validate.validateProfileAssociated(data)
    if not result["Valid"]:
        return jsonify({"msg": result["message"]}), 400
    auth.edit_profile_user(user, data)
    associates.edit_profile_associated(user.associated[0], data)
    return jsonify({"msg": "Descripción actualizada"}), 200


@api_blueprint.post("/me/profile/photo")
@jwt_required()
def act_img_profile():
    """Actualiza la foto de usuario"""

    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]

    data = request.get_json()
    if not data["photo"]:
        return jsonify({"msg": "No se mando ninguna foto"}), 400

    auth.save_base64_user(data["photo"], user.email)

    return jsonify({"msg": "Foto actualizada"}), 200


@api_blueprint.get("/club/data/defaulters")
def stat_defaulters():
    """Retorna la cantidad de asociados morosos y no morosos actuales."""
    associates_ret = associates.list_associated()
    defaulters = 0
    non_defaulters = 0
    for each in associates_ret:
        if associates.is_defaulter(each.id):
            defaulters += 1
        else:
            non_defaulters += 1

    return jsonify({"defaulters": defaulters, "non_defaulters": non_defaulters}), 200


@api_blueprint.get("/sport/data/genders/<int:num>")
def stat_sport_gender(num):
    """Retorna la distribucion de generos de la disciplina indicada por id."""
    # sport_id = request.headers.get("sport_id")
    sport_id = num

    # Verificar que se haya incluido un id
    # if not sport_id:
    #     return jsonify({"msg": "Falta la id de la disciplina"}), 404

    # Verificar que id sea un numero
    # if not sport_id.isdigit():
    #     return jsonify({"msg": "Id no es un numero"}), 404

    sport = sports.get_sport_by_id_no_404(sport_id)

    # Verificar que id corresponda a una disciplina
    if not sport:
        return jsonify({"msg": "Id no es una disciplina valida"}), 404

    ms = 0
    fs = 0
    os = 0

    for each in sport.associates:
        if each.gender == "M":
            ms += 1
        elif each.gender == "F":
            fs += 1
        else:
            os += 1

    return jsonify({"males": ms, "females": fs, "others": os}), 200


@api_blueprint.get("/sports/data/genders")
def stat_sports_genders():
    """Retorna la distribucion de generos de la disciplina indicada por id."""
    sports_ret = sports.list_enabled_sports()

    sports_names = []
    # Tengo que armar los arreglos como los datasets para el grafico
    males = []
    females = []
    others = []

    for sport in sports_ret:
        ms = 0
        fs = 0
        os = 0
        for associate in sport.associates:
            if associate.gender == "M":
                ms += 1
            elif associate.gender == "F":
                fs += 1
            else:
                os += 1
        males.append(ms)
        females.append(fs)
        others.append(os)
        sports_names.append(sport.name + " " + sport.division)

    genders_ret = [males, females, others]

    return jsonify({
        "genders": genders_ret, "sport_names": sports_names}), 200


@api_blueprint.get("/club/data/associates")
def stat_associates():
    """Retorna la cantidad de asociados/cuotas por mes del año actual."""
    # year = request.headers.get("year")

    #   if year:
    #       if not year.isdigit():
    #           return jsonify({"msg": "El año no es un numero"})
    #       year = int(year)
    #       if not year < datetime.today().year:
    #           return jsonify({"msg": "El año no es valido"})
    #       if not year > datetime(2020, 1, 1).year:
    #           return jsonify({"msg": "El año no es valido"})

    #   else:
    #       year = datetime.today().year

    quotas_ret = quotas.list_year_quotas(datetime.today().year)
    monthly_members = [0 for i in range(12)]
    for each in quotas_ret:
        # Medio raro, pero toma la fecha de vencimiento, resta un mes, toma el
        # mes solo y le resta uno para compensar por las posiciones del arreglo
        # empezando en 0. Al valor en esa posicion lo incrementa en 1
        monthly_members[(each.end_date - relativedelta(months=1)).month - 1] += 1

    return jsonify({"monthly_members": monthly_members}), 200


@api_blueprint.get("/club/associated/<int:nro_associated>")
def get_associated_by_id(nro_associated):
    """Retorna la informacion de un asociado a partir de un numero de asociado"""
    if not nro_associated:
        return jsonify({"msg": "Falta la nro de asociado"}), 404
    associated = associates.get_associated_by_id(int(nro_associated))
    associated_info = {}
    if associated:
        my_sports = []
        for s in associated.sports:
            my_sports.append(s.name)
        defeated_quotas = get_quotas_by_state_by_associated_id(associated.id, False)
        associated_info = {
            "name": associated.name,
            "sports": my_sports,
            "defeated_quotas": len(defeated_quotas),
        }
        return jsonify(associated_info), 200
    else:
        return jsonify({"msg": "No se encontro asociado con ese numero"}), 404


@api_blueprint.get("/me/profile/history")
@jwt_required()
def associated_activity():
    """Retorna la cantidad de disciplinas que el asociado lleva inscriptas en los ultimos 12 meses"""

    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]

    # seteo la fecha de inicio para hace 1 año, pero apartir del dia 11,
    # para no traerme las cuotas que vencian ese mes que corresponden a disciplinas del mes anterior
    year = datetime.today().year - 1
    month = datetime.today().month
    day = 11
    first_date = datetime(year, month, day)

    # seteo la fecha 'hasta' sumandole un mes a la fecha actual,
    # ya que si estamos a principio de mes no se traeria las cuotas que vencen el 10
    last_date = datetime.today() + relativedelta(months=1)

    quotas_ret = quotas.list_Quotas_associatedID_by_range_date(
        user.associated[0].id, first_date, last_date
    )
    monthly_activity = [0 for i in range(12)]

    ArrMonth, posMonth = array_last_months()

    for each in quotas_ret:
        data = QuotaJson.fromJSON(each.dataJSON)
        monthly_activity[
            posMonth[(each.end_date - relativedelta(months=1)).month - 1]
        ] = len(data.sports)
    return jsonify({"monthly_activity": monthly_activity, "ArrMonth": ArrMonth}), 200


@api_blueprint.get("/me/credential")
@jwt_required()
def get_my_credential():
    """Retorna los datos de la credencial de un asociado"""
    current_user = get_jwt_identity()

    user = auth.find_user_by_mail(current_user).items[0]
    role = auth.find_role_by_name("socio")

    # Verificar que el usuario posee rol socio
    if role not in user.role:
        return (
            jsonify({"msg": "Socio no registrado"}),
            403,
        )

    # Verificar que el usuario posee un asociado
    if not user.associated[0]:
        return (
            jsonify({"msg": "No se encontró ningún asociado"}),
            404,
        )

    license_id = user.associated[0].credential[0].id
    my_license = licenses.get_license_by_id(license_id)

    if not my_license:
        return (
            jsonify({"msg": "No tiene licencia"}),
            405,
        )
    photo = (
        "https://admin-grupo17.proyecto2022.linti.unlp.edu.ar/public/images/users/"
        + my_license.photo
    )
    qr = (
        "https://admin-grupo17.proyecto2022.linti.unlp.edu.ar/public/images/qr/"
        + my_license.qr
    )
    estado = associates.is_defaulter(user.associated[0].id)
    fecha =  user.associated[0].discharge_date.strftime('%d-%m-%Y')

    json_data = {
        "photo": photo,
        "start_date": my_license.discharge_date,
        "qr": qr,
        "name": user.associated[0].name,
        "surname": user.associated[0].surname,
        "document_number": user.associated[0].document_number,
        "id": user.associated[0].id,
        "discharge_date": fecha,
        "estado": estado
    }

    return json_data


@api_blueprint.get("/club/data/info_and_contact")
def info_and_contact():
    """Retorna la descripción del home e información de contacto"""
    config = setting.get_setting()
    descHome = config.description_home
    emailContact = config.contact_email
    celContact = config.contact_info

    return (
        jsonify(
            {
                "descHome": descHome,
                "emailContact": emailContact,
                "celContact": celContact,
            }
        ),
        200,
    )
