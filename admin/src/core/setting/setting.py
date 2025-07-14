from datetime import datetime

from src.core.database import db


class Setting(db.Model):

    __tablename__ = "setting"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cant_elements_page = db.Column(db.Integer, nullable=False)
    enable_pay_table = db.Column(db.Boolean, nullable=False)
    contact_info = db.Column(db.String(300), nullable=False)
    contact_email = db.Column(db.String(50), unique=True, nullable=False, default="-")
    voucher_title = db.Column(db.String(100), nullable=False)
    price_month = db.Column(db.Float, nullable=False)
    percent_increase_debtors = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String(10), nullable=False)
    description_home = db.Column(db.String(300), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
