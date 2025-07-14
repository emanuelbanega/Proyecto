from src.core.payments.paymentV2 import PaymentV2
from src.core.database import db
from src.core.associates import Associated, add_associated
import os
import base64
from random import sample
from flask import current_app



def add_payment(**kwargs):
    # Creo un nuevo pago en la base de datos.
    payment = PaymentV2(**kwargs)
    db.session.add(payment)
    db.session.commit()
    return payment

def save_base64_payment(file_content, extension, payment):
    newNameFile = stringRandom() + "." + extension
    try:
        file_content = base64.b64decode(file_content)
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], "images/payments", newNameFile)
        with open(path, "wb") as f:
            f.write(file_content)
            f.close()
    except Exception as e:
        print(str(e))
    else:
        payment.voucher_image = newNameFile
        db.session.commit()

def confirm_payment(payment):
    payment.state = True
    db.session.commit()
    return payment

def decline_payment(payment):
    payment.quotas[0].state = False
    delete_payment(payment)

def stringRandom():
    """Genera un string aleatorio"""
    string_random = "0123456789abcdefghijkmnopqrstuvwxyz_"
    long = 20
    sequence = string_random.upper()
    result_random = sample(sequence, long)
    string_random = "".join(result_random)
    return string_random

def append_quota(payment, quota):
    payment.quotas.append(quota)
    db.session.commit()
    return payment


def delete_payment(payment):
    # Elimina un pago en la base de datos.
    db.session.delete(payment)
    db.session.commit()
    return payment


def find_payment_by_id_associated(id):
    result = []
    for p in list_payment():
        if p.quotas[0].associated_id == id:
            result.append(p)
    return result


def find_associated_by_active(active, current_page, items):
    # Trae de la BD los asociados paginados con el estado = 'active'. Current_page es la pagina actual, items los elementos a mostrar.
    return (
        Associated.query.filter_by(condition=active)
        .order_by(Associated.id)
        .paginate(page=current_page, per_page=items)
    )


def find_payment_by_id(id, cant, current_page):
    aux = ()
    for i in list_payment():
        if i.quotas[0].associated_id == id:
            aux = aux + (i.id,)
    return PaymentV2.query.filter(PaymentV2.id.in_(aux)).paginate(
        page=current_page, per_page=cant
    )


def find_payment_by_surname(surname, cant, current_page):
    aux = ()
    for i in list_payment():
        if i.quotas[0].associates.surname == surname:
            aux = aux + (i.id,)
    return PaymentV2.query.filter(PaymentV2.id.in_(aux)).paginate(
        page=current_page, per_page=cant
    )


def get_payment_by_id(id):
    # Busca y retorna un pago por id.
    payment = PaymentV2.query.get_or_404(id)
    return payment


def list_payment():
    # Trae todos los pagos de la base de datos.
    return PaymentV2.query.all()


def list_payments_page(current_page, items):
    # Trae los pagos de la pagina idicada con el numero de items por pagina indicado.
    return PaymentV2.query.order_by(PaymentV2.id).paginate(
        page=current_page, per_page=items
    )

def update_payment(payment):
    # Modifica el pago con el dato enviado por parametro
    db.session.commit()
    return payment

def get_pending_payments():
    return PaymentV2.query.filter_by(state=False)