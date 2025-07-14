import json
from datetime import datetime
from unicodedata import name
from src.core import auth
from src.core import sports
from src.core import associates
from src.core.database import bcrypt
from src.core import setting
from src.core.quotas import quotaV2
from src.core.payments import paymentV2
from src.core import payments


def run():

    # Cargar usuarios

    print("Cargando usuarios...")
    passGenerica = bcrypt.generate_password_hash("1234asdf").decode("utf-8")
    user1 = auth.create_User(
        email="messi@gmail.com",
        userName="LeoM",
        password=passGenerica,
        active=True,
        photo="usuario.jpg",
        first_name="Lionel",
        last_name="Messi",
    )
    user2 = auth.create_User(
        email="nico_r@gmail.com",
        userName="NicoR",
        password=passGenerica,
        active=True,
        first_name="Nicolás",
        last_name="Romero",
    )
    user3 = auth.create_User(
        email="pablo@gmail.com",
        userName="PabloV",
        password=passGenerica,
        active=False,
        first_name="Pablo",
        last_name="Valero",
    )
    user4 = auth.create_User(
        email="ema_banega@gmail.com",
        userName="EmaB",
        password=passGenerica,
        active=True,
        photo="yo.jpg",
        first_name="Luis Emanuel",
        last_name="Banega",
    )
    user5 = auth.create_User(
        email="lautaro@gmail.com",
        userName="LauG",
        password=passGenerica,
        active=True,
        first_name="Lautaro Julian",
        last_name="Molina Garcia",
    )
    user6 = auth.create_User(
        email="usuarinoactivo@gmail.com",
        userName="AsociadoNoActivo",
        password=passGenerica,
        active=True,
        first_name="Soy una Prueba",
        last_name="De Borrado",
    )
    user7 = auth.create_User(
        email="user7@gmail.com",
        userName="user7",
        password=passGenerica,
        active=True,
        first_name="Julian",
        last_name="Mañas",
    )
    user8 = auth.create_User(
        email="user8@gmail.com",
        userName="user8",
        password=passGenerica,
        active=True,
        first_name="Micaela",
        last_name="Kaur",
    )
    user9 = auth.create_User(
        email="user9@gmail.com",
        userName="user9",
        password=passGenerica,
        active=True,
        first_name="Teodora",
        last_name="Palacios",
    )
    user10 = auth.create_User(
        email="user10@gmail.com",
        userName="user10",
        password=passGenerica,
        active=True,
        first_name="Roberto",
        last_name="Gallego",
    )
    user11 = auth.create_User(
        email="user11@gmail.com",
        userName="user11",
        password=passGenerica,
        active=True,
        first_name="Mariana",
        last_name="Guisado",
    )
    user12 = auth.create_User(
        email="user12@gmail.com",
        userName="user12",
        password=passGenerica,
        active=True,
        first_name="Roser",
        last_name="Carvajal",
    )
    user13 = auth.create_User(
        email="user13@gmail.com",
        userName="user13",
        password=passGenerica,
        active=True,
        first_name="Nicolás",
        last_name="Brito",
    )
    user14 = auth.create_User(
        email="user14@gmail.com",
        userName="user14",
        password=passGenerica,
        active=True,
        first_name="Aleix",
        last_name="Revilla",
    )
    user15 = auth.create_User(
        email="user15@gmail.com",
        userName="user15",
        password=passGenerica,
        active=True,
        first_name="Said",
        last_name="Ribas",
    )
    user16 = auth.create_User(
        email="user16@gmail.com",
        userName="user16",
        password=passGenerica,
        active=True,
        first_name="Hector",
        last_name="Juan",
    )
    user17 = auth.create_User(
        email="user17@gmail.com",
        userName="user17",
        password=passGenerica,
        active=True,
        first_name="Adriana",
        last_name="Palomares",
    )

    # Cargar roles

    print("Cargando roles...")
    role1 = auth.create_Role(
        name="administrador",
    )
    role2 = auth.create_Role(
        name="operador",
    )
    role3 = auth.create_Role(
        name="socio",
    )

    # Cargar disciplinas
    print("Cargando disciplinas...")

    sport1 = sports.add_sport(
        name="Futbol",
        division="Sub 20",
        instructors_names="Carlos Gomez",
        schedule="Lunes 15 a 16, Miercoles 14 a 15",
        monthly_fee="2000",
        enabled=True,
    )

    sport2 = sports.add_sport(
        name="Basket",
        division="Pre-mini",
        instructors_names="Juan Perez, Andrea Dolivar",
        schedule="Martes 10 a 11, Jueves 13 a 14, Sabado 10 a 11",
        monthly_fee="1500",
        enabled=False,
    )

    sport3 = sports.add_sport(
        name="Volley",
        division="Mini",
        instructors_names="Andrea Dolivar",
        schedule="Miercoles 13 a 14",
        monthly_fee="1700",
        enabled=True,
    )

    sport4 = sports.add_sport(
        name="Futbol",
        division="Pre-mini",
        instructors_names="Carlos Gomez",
        schedule="Viernes de 16 a 17",
        monthly_fee="2200",
        enabled=False,
    )

    sport5 = sports.add_sport(
        name="Futbol",
        division="Sub 19",
        instructors_names="Carlos Gomez",
        schedule="Miercoles de 16 a 17",
        monthly_fee="760",
        enabled=True,
    )

    sport6 = sports.add_sport(
        name="Volley",
        division="juvenil",
        instructors_names="David Tamayo Guijarro",
        schedule="Lunes de 9 a 10:30",
        monthly_fee="1900",
        enabled=True,
    )

    sport7 = sports.add_sport(
        name="Béisbol",
        division="Infantil",
        instructors_names="Carolina Izaguirre Gordillo",
        schedule="Sabados de 14 a 15",
        monthly_fee="1200",
        enabled=False,
    )

    sport8 = sports.add_sport(
        name="Tenis",
        division="Cadete",
        instructors_names="Elvira Diéguez Bolaños",
        schedule="Viernes de 16 a 17",
        monthly_fee="2200",
        enabled=True,
    )

    # Cargar asociados
    print("Cargando asociados..")
    associated1 = associates.add_associated(
        name="Luis Emanuel",
        surname="Banega",
        document_type="DNI",
        document_number="42631018",
        gender="M",
        direction="Calle 62 N°577",
        condition="Activo",
        phone="2245404830",
        mail="emabanega@hotmail.com",
    )
    associated2 = associates.add_associated(
        name="Jose",
        surname="Lopez",
        document_type="LE",
        document_number="42543123",
        gender="Otro",
        direction="Calle 62 N°577",
        condition="No-activo",
    )
    associated3 = associates.add_associated(
        name="Jose",
        surname="Baeza",
        document_type="DNI",
        document_number="32188085",
        gender="M",
        direction="Calle 11 N°577",
        condition="Activo",
    )
    associated4 = associates.add_associated(
        name="Fidela",
        surname="Arroyo",
        document_type="LC",
        document_number="36318492",
        gender="F",
        direction="Calle 62 N°1231",
        condition="Activo",
    )
    associated5 = associates.add_associated(
        name="Micaela",
        surname="Kaur",
        document_type="DNI",
        document_number="47442969",
        gender="F",
        direction="Calle 44 N°13",
        condition="No-activo",
    )
    associated6 = associates.add_associated(
        name="Teodora",
        surname="Palacios",
        document_type="DNI",
        document_number="39640847",
        gender="F",
        direction="Calle 42 N°2321",
        condition="No-activo",
    )
    associated7 = associates.add_associated(
        name="Julian",
        surname="Mañas",
        document_type="LE",
        document_number="30438523",
        gender="M",
        direction="Calle 13 N°666",
        condition="Activo",
    )
    associated8 = associates.add_associated(
        name="Aarón",
        surname="Padilla Carlos",
        document_type="LC",
        document_number="43113623",
        gender="M",
        direction="Calle 1 N°423",
        condition="Activo",
    )

    associated9 = associates.add_associated(
        name="Roberto",
        surname="Gallego",
        document_type="DNI",
        document_number="29221696",
        gender="M",
        direction="Calle 10 N°221",
        condition="Activo",
    )

    associated10 = associates.add_associated(
        name="Mariana",
        surname="Guisado",
        document_type="DNI",
        document_number="26129437",
        gender="F",
        direction="Calle 38 N°1601",
        condition="Activo",
    )

    associated11 = associates.add_associated(
        name="Roser",
        surname="Carvajal",
        document_type="DNI",
        document_number="36849608",
        gender="M",
        direction="Calle 33 N°1837",
        condition="Activo",
    )

    associated12 = associates.add_associated(
        name="Nicolás",
        surname="Brito",
        document_type="DNI",
        document_number="35693803",
        gender="M",
        direction="Calle 19 N°1918",
        condition="Activo",
    )

    associated13 = associates.add_associated(
        name="Aleix",
        surname="Revilla",
        document_type="DNI",
        document_number="29365104",
        gender="F",
        direction="Calle 28 N°401",
        condition="Activo",
    )

    associated14 = associates.add_associated(
        name="Said",
        surname="Ribas",
        document_type="DNI",
        document_number="30727440",
        gender="M",
        direction="Calle 41 N°1131",
        condition="Activo",
    )

    associated15 = associates.add_associated(
        name="Hector",
        surname="Juan",
        document_type="DNI",
        document_number="43551926",
        gender="M",
        direction="Calle 16 N°1957",
        condition="Activo",
    )

    associated16 = associates.add_associated(
        name="Adriana",
        surname="Palomares",
        document_type="DNI",
        document_number="41543446",
        gender="M",
        direction="Calle 11 N°201",
        condition="Activo",
    )

    # genera un par de cuotas

    cuotaJsonV2_1 = {
        "currency_type": "ARS",
        "membership_amount": 2000.0,
        "surcharge": 20,
        "sports": [
            {"Name": "Tenis", "division": "Cadete", "monthly_fee": 2200},
            {"Name": "Volley", "division": "juvenil", "monthly_fee": 1900},
        ],
        "total_amount": 6100,
    }

    cuotaJsonV2_2 = {
        "currency_type": "ARS",
        "membership_amount": 2000.0,
        "surcharge": 20,
        "sports": [
            {"Name": "Futbol", "division": "Sub 19", "monthly_fee": 760},
        ],
        "total_amount": 2760,
    }

    cuotaJsonV2_3 = {
        "currency_type": "ARS",
        "membership_amount": 1500.0,
        "surcharge": 20,
        "sports": [
            {"Name": "Tenis", "division": "Cadete", "monthly_fee": 2200},
        ],
        "total_amount": 3700,
    }

    cuotaJsonV2_4 = {
        "currency_type": "ARS",
        "membership_amount": 1500.0,
        "surcharge": 20,
        "sports": [
            {"Name": "Tenis", "division": "Cadete", "monthly_fee": 2200},
        ],
        "total_amount": 3700,
    }

    cuotaJsonV2_5 = {
        "currency_type": "ARS",
        "membership_amount": 1500.0,
        "surcharge": 20,
        "sports": [
            {"Name": "Tenis", "division": "Cadete", "monthly_fee": 2200},
            {"Name": "Futbol", "division": "Sub 19", "monthly_fee": 760},
            {"Name": "Volley", "division": "juvenil", "monthly_fee": 1900},
        ],
        "total_amount": 6360,
    }

    print("Cargando cuotas...")
    cutaV2_1 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_1),
        end_date=datetime(2022, 9, 10, 23, 59, 59, 00000),
        associates=associated8,
    )

    cutaV2_2 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_2),
        end_date=datetime(2022, 10, 10, 23, 59, 59, 00000),
        associates=associated8,
    )

    cutaV2_3 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_3),
        end_date=datetime(2022, 11, 10, 23, 59, 59, 00000),
        associates=associated8,
    )

    cutaV2_4 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 5, 10, 23, 59, 59, 00000),
        associates=associated10,
    )

    cutaV2_5 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 6, 10, 23, 59, 59, 00000),
        associates=associated10,
    )

    cutaV2_6 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_5),
        end_date=datetime(2022, 7, 10, 23, 59, 59, 00000),
        associates=associated10,
    )

    cutaV2_7 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 8, 10, 23, 59, 59, 00000),
        associates=associated10,
    )

    cutaV2_8 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 9, 10, 23, 59, 59, 00000),
        associates=associated10,
    )

    cutaV2_9 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 10, 10, 23, 59, 59, 00000),
        associates=associated10,
    )

    cutaV2_10 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 11, 10, 23, 59, 59, 00000),
        associates=associated10,
    )
    cutaV2_11 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 1, 10, 23, 59, 59, 00000),
        associates=associated14,
    )
    cutaV2_12 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 6, 10, 23, 59, 59, 00000),
        associates=associated14,
    )
    cutaV2_13 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 2, 10, 23, 59, 59, 00000),
        associates=associated14,
    )
    cutaV2_14 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 5, 10, 23, 59, 59, 00000),
        associates=associated14,
    )
    cutaV2_15 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 11, 10, 23, 59, 59, 00000),
        associates=associated14,
    )
    cutaV2_16 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2022, 11, 10, 23, 59, 59, 00000),
        associates=associated16,
    )
    # Cuotas para testeo de api
    cutaV2_17 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2023, 1, 10, 23, 59, 59, 00000),
        associates=associated16,
    )
    cutaV2_18 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2021, 2, 10, 23, 59, 59, 00000),
        associates=associated16,
    )
    cutaV2_19 = quotaV2.create_Quota(
        dataJSON=json.dumps(cuotaJsonV2_4),
        end_date=datetime(2021, 1, 10, 23, 59, 59, 00000),
        associates=associated16,
    )

    print("Cargando facturas...")
    paymentV2_1 = paymentV2.create_Payment(
        orden=1001,
        amount=quotaV2.get_detail_quota(cutaV2_1.id).total_amount,
        state=True,
    )
    paymentV2_2 = paymentV2.create_Payment(
        orden=1004,
        amount=quotaV2.get_detail_quota(cutaV2_4.id).total_amount,
        state=True,
    )
    paymentV2_3 = paymentV2.create_Payment(
        orden=1005,
        amount=quotaV2.get_detail_quota(cutaV2_5.id).total_amount,
        state=True,
    )
    paymentV2_4 = paymentV2.create_Payment(
        orden=1006,
        amount=quotaV2.get_detail_quota(cutaV2_6.id).total_amount,
        state=True,
    )
    paymentV2_5 = paymentV2.create_Payment(
        orden=1007,
        amount=quotaV2.get_detail_quota(cutaV2_7.id).total_amount,
        state=True,
    )
    paymentV2_6 = paymentV2.create_Payment(
        orden=1008,
        amount=quotaV2.get_detail_quota(cutaV2_8.id).total_amount,
        state=True,
    )
    paymentV2_7 = paymentV2.create_Payment(
        orden=1009,
        amount=quotaV2.get_detail_quota(cutaV2_9.id).total_amount,
        state=True,
    )
    paymentV2_8 = paymentV2.create_Payment(
        orden=1010,
        amount=quotaV2.get_detail_quota(cutaV2_10.id).total_amount,
        state=True,
    )
    paymentV2_9 = paymentV2.create_Payment(
        orden=1011,
        amount=quotaV2.get_detail_quota(cutaV2_11.id).total_amount,
        state=True,
    )
    paymentV2_10 = paymentV2.create_Payment(
        orden=1012,
        amount=quotaV2.get_detail_quota(cutaV2_12.id).total_amount,
        state=True,
    )
    paymentV2_11 = paymentV2.create_Payment(
        orden=1013,
        amount=quotaV2.get_detail_quota(cutaV2_13.id).total_amount,
        state=True,
    )
    paymentV2_12 = paymentV2.create_Payment(
        orden=1014,
        amount=quotaV2.get_detail_quota(cutaV2_14.id).total_amount,
        state=True,
    )
    paymentV2_13 = paymentV2.create_Payment(
        orden=1015,
        amount=quotaV2.get_detail_quota(cutaV2_15.id).total_amount,
        state=True,
    )
    paymentV2_14 = paymentV2.create_Payment(
        orden=1016,
        amount=quotaV2.get_detail_quota(cutaV2_16.id).total_amount,
        state=True,
    )
    paymentV2_15 = paymentV2.create_Payment(
        orden=1002,
        amount=quotaV2.get_detail_quota(cutaV2_2.id).total_amount,
        state=True,
    )

    print("Asignando cuotas a facturas...")
    quotaV2.assign_payment(cutaV2_1, paymentV2_1)
    quotaV2.assign_payment(cutaV2_2, paymentV2_15)
    quotaV2.assign_payment(cutaV2_4, paymentV2_2)
    quotaV2.assign_payment(cutaV2_5, paymentV2_3)
    quotaV2.assign_payment(cutaV2_6, paymentV2_4)
    quotaV2.assign_payment(cutaV2_7, paymentV2_5)
    quotaV2.assign_payment(cutaV2_8, paymentV2_6)
    quotaV2.assign_payment(cutaV2_9, paymentV2_7)
    quotaV2.assign_payment(cutaV2_10, paymentV2_8)
    quotaV2.assign_payment(cutaV2_11, paymentV2_9)
    quotaV2.assign_payment(cutaV2_12, paymentV2_10)
    quotaV2.assign_payment(cutaV2_13, paymentV2_11)
    quotaV2.assign_payment(cutaV2_14, paymentV2_12)
    quotaV2.assign_payment(cutaV2_15, paymentV2_13)
    quotaV2.assign_payment(cutaV2_16, paymentV2_14)

    # asigna los asociados a las disciplinas
    print("Inscribiendo asociados...")

    sports.append_to_associates(sport1, associated1)
    sports.append_to_associates(sport3, associated1)
    sports.append_to_associates(sport1, associated4)
    sports.append_to_associates(sport8, associated3)
    sports.append_to_associates(sport1, associated7)
    sports.append_to_associates(sport3, associated9)
    sports.append_to_associates(sport5, associated10)
    sports.append_to_associates(sport6, associated11)
    sports.append_to_associates(sport8, associated12)
    sports.append_to_associates(sport3, associated13)
    sports.append_to_associates(sport5, associated14)
    sports.append_to_associates(sport1, associated15)
    sports.append_to_associates(sport5, associated16)

    # Cargar permisos

    print("Cargando permisos...")
    permission1 = auth.create_Permission(
        name="start_session_web_admin",
    )
    permission2 = auth.create_Permission(
        name="users_index",
    )
    permission3 = auth.create_Permission(
        name="users_new",
    )
    permission4 = auth.create_Permission(
        name="users_destroy",
    )
    permission5 = auth.create_Permission(
        name="users_update",
    )
    permission6 = auth.create_Permission(
        name="users_show",
    )
    permission7 = auth.create_Permission(
        name="users_status",
    )

    # Cargando permisos de disciplinas
    permission8 = auth.create_Permission(
        name="sports_index",
    )
    permission9 = auth.create_Permission(
        name="sports_new",
    )
    permission10 = auth.create_Permission(
        name="sports_destroy",
    )
    permission11 = auth.create_Permission(
        name="sports_update",
    )
    permission12 = auth.create_Permission(
        name="sports_show",
    )

    # Cargando permisos de asociados
    permission13 = auth.create_Permission(
        name="associates_index",
    )
    permission14 = auth.create_Permission(
        name="associates_new",
    )
    permission15 = auth.create_Permission(
        name="associates_destroy",
    )
    permission16 = auth.create_Permission(
        name="associates_update",
    )
    permission17 = auth.create_Permission(
        name="associates_show",
    )

    # Cargando permisos de inscipcion
    permission18 = auth.create_Permission(name="signup_new")
    permission19 = auth.create_Permission(name="signup_destroy")
    permission20 = auth.create_Permission(name="signup_list")

    # Cargando permisos de cuotas
    permission21 = auth.create_Permission(name="quota_index")
    permission22 = auth.create_Permission(name="quota_show")
    permission23 = auth.create_Permission(name="quota_new")
    permission24 = auth.create_Permission(name="quota_generate")

    # Cargando permisos de carnet

    permission25 = auth.create_Permission(name="carnet_new")
    permission26 = auth.create_Permission(name="carnet_view")
    # Asignando roles a usuarios

    print("Relacionando usuarios con roles...")
    auth.assign_role(user1, role1)
    auth.assign_role(user2, role2)
    auth.assign_role(user2, role3)
    auth.assign_role(user3, role2)
    auth.assign_role(user4, role1)
    auth.assign_role(user4, role3)
    auth.assign_role(user5, role2)
    auth.assign_role(user6, role3)
    auth.assign_role(user7, role3)
    auth.assign_role(user8, role3)
    auth.assign_role(user9, role3)
    auth.assign_role(user10, role3)
    auth.assign_role(user11, role3)
    auth.assign_role(user12, role3)
    auth.assign_role(user13, role3)
    auth.assign_role(user14, role3)
    auth.assign_role(user15, role3)
    auth.assign_role(user16, role3)
    auth.assign_role(user17, role3)

    # Asignando permisos a roles

    print("Relacionando permisos con roles...")
    auth.assign_permission(permission1, role1)
    auth.assign_permission(permission1, role2)
    auth.assign_permission(permission2, role1)
    auth.assign_permission(permission3, role1)
    auth.assign_permission(permission4, role1)
    auth.assign_permission(permission5, role1)
    auth.assign_permission(permission6, role1)
    auth.assign_permission(permission7, role1)

    # Permisos de disciplinas
    # Administrador
    auth.assign_permission(permission8, role1)
    auth.assign_permission(permission9, role1)
    auth.assign_permission(permission10, role1)
    auth.assign_permission(permission11, role1)
    auth.assign_permission(permission12, role1)
    auth.assign_permission(permission13, role1)
    auth.assign_permission(permission14, role1)
    auth.assign_permission(permission15, role1)
    auth.assign_permission(permission16, role1)
    auth.assign_permission(permission17, role1)
    # Operador
    auth.assign_permission(permission8, role2)
    auth.assign_permission(permission9, role2)
    auth.assign_permission(permission11, role2)
    auth.assign_permission(permission12, role2)
    auth.assign_permission(permission13, role2)
    auth.assign_permission(permission14, role2)
    auth.assign_permission(permission16, role2)

    # Permisos de inscripcion
    # Administrador
    auth.assign_permission(permission18, role1)
    auth.assign_permission(permission19, role1)
    auth.assign_permission(permission20, role1)
    # Operador
    auth.assign_permission(permission18, role2)
    auth.assign_permission(permission19, role2)
    auth.assign_permission(permission20, role2)

    # Permisos de cuotas
    # Administrador
    auth.assign_permission(permission21, role1)
    auth.assign_permission(permission22, role1)
    auth.assign_permission(permission23, role1)
    auth.assign_permission(permission24, role1)

    # Operador
    auth.assign_permission(permission21, role2)
    auth.assign_permission(permission22, role2)
    auth.assign_permission(permission23, role2)

    # Permisos de carnet
    # Administrador
    auth.assign_permission(permission25, role1)
    auth.assign_permission(permission26, role1)

    # Operador
    auth.assign_permission(permission25, role2)
    auth.assign_permission(permission26, role2)

    # Configuracion

    print("Cargando Configuracion...")

    settingObj = setting.create_setting(
        cant_elements_page=5,
        enable_pay_table=False,
        contact_info="Cel:0002222",
        contact_email="clubsocio_contacto@clubsocio.com",
        voucher_title="ReciboClubV1",
        price_month=2000,
        percent_increase_debtors=20,
        currency_type="ARS",
        description_home="Hazte socio del club para estar al tanto de las últimas novedades y disfruta de todas nuestras disciplinas",
    )

    # asignar asociado a cuenta socio
    print("Asignando asociados a socios...")
    auth.verify_asig_associate(user4, associated1)
    auth.verify_asig_associate(user6, associated2)
    auth.verify_asig_associate(user7, associated7)
    auth.verify_asig_associate(user8, associated5)
    auth.verify_asig_associate(user9, associated6)
    auth.verify_asig_associate(user10, associated9)
    auth.verify_asig_associate(user11, associated10)
    auth.verify_asig_associate(user12, associated11)
    auth.verify_asig_associate(user13, associated12)
    auth.verify_asig_associate(user14, associated13)
    auth.verify_asig_associate(user15, associated14)
    auth.verify_asig_associate(user16, associated15)
    auth.verify_asig_associate(user17, associated16)
