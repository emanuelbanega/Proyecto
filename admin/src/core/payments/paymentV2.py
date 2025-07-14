from datetime import datetime
from src.core.associates import associated
from src.core.database import db


class PaymentV2(db.Model):

    __tablename__ = "paymentsV2"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    orden = db.Column(db.Integer, nullable=False)
    quotas = db.relationship("Quota", back_populates="payment")
    amount = db.Column(db.Float, nullable=False)
    state = db.Column(db.Boolean, nullable=False)
    voucher_image = db.Column(db.String(100), nullable=True, default=None)


def create_Payment(**kwargs):
    """Agrega un pago a la BD"""
    payment = PaymentV2(**kwargs)
    db.session.add(payment)
    db.session.commit()

    return payment
