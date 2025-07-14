import json
from datetime import datetime

from src.core.database import db
from src.core import associates
from src.core import sports
from src.core import setting


class DataSport:
    def __init__(self):
        self.Name = ""
        self.division = ""
        self.monthly_fee = 0


class QuotaJson:
    def __init__(self):
        self.currency_type = ""
        self.surcharge = 0
        self.membership_amount = 0
        self.total_amount = 0
        self.sports = []

    @staticmethod
    def fromJSON(dataJSON):
        aux = QuotaJson()
        jsonOBJ = json.loads(dataJSON)
        aux.currency_type = jsonOBJ["currency_type"]
        aux.surcharge = jsonOBJ["surcharge"]
        aux.membership_amount = jsonOBJ["membership_amount"]
        aux.total_amount = jsonOBJ["total_amount"]
        for sport in jsonOBJ["sports"]:
            auxSport = DataSport()
            auxSport.Name = sport["Name"]
            auxSport.division = sport["division"]
            auxSport.monthly_fee = sport["monthly_fee"]
            aux.sports.append(auxSport)
        return aux

    @staticmethod
    def fromObject(associated):
        config = setting.get_setting()
        total = config.price_month
        sportJson = []
        for sport in associated.sports:
            sportJson.append(
                {
                    "Name": sport.name,
                    "division": sport.division,
                    "monthly_fee": float(sport.monthly_fee),
                }
            )
            total += float(sport.monthly_fee)
        datos_JSON = {
            "currency_type": config.currency_type,
            "membership_amount": config.price_month,
            "surcharge": config.percent_increase_debtors,
            "sports": sportJson,
            "total_amount": total,
        }
        return datos_JSON


class Quota(db.Model):

    __tablename__ = "quotas"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    end_date = db.Column(db.DateTime, nullable=False)
    associated_id = db.Column(db.Integer, db.ForeignKey("associates.id"))
    associates = db.relationship("Associated", back_populates="quotas")
    state = db.Column(db.Boolean, nullable=False, default=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("paymentsV2.id"))
    payment = db.relationship("PaymentV2", back_populates="quotas")
    dataJSON = db.Column(db.String(500), nullable=False)
    final_amount = 0


def get_quotas():
    """Retorna todas las cuotas."""
    return Quota.query.all()


def create_Quota(**kwargs):
    """Agrega una cuota a la BD, recibe end_date, associates, dataJSON"""
    quota = Quota(**kwargs)
    db.session.add(quota)
    db.session.commit()

    return quota


def assign_payment(quota, payment):
    """Agrega un asociado a la disciplina."""
    quota.payment = payment
    quota.state = True
    db.session.commit()
    return quota


def get_quota_by_id(id_quota):
    quota = Quota.query.filter_by(id=id_quota).first()
    return quota


def get_quotas_by_associated_id(id):
    quotas = Quota.query.filter_by(associated_id=id).all()
    return quotas


def get_quotas_by_state_by_associated_id(idAssociated, stateQuota):
    """devuelve las cuotas segun su estado del asociado"""
    quotas = Quota.query.filter_by(associated_id=idAssociated, state=stateQuota).all()
    return quotas


def get_detail_quota(id_quota):
    quota = Quota.query.filter_by(id=id_quota).first()
    if quota:
        return QuotaJson.fromJSON(quota.dataJSON)
    return None
