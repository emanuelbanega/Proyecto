from datetime import datetime
from src.core.database import db


class Associated(db.Model):

    __tablename__ = "associates"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    document_type = db.Column(db.String(5), nullable=False)
    document_number = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(4), nullable=False)
    direction = db.Column(db.String(30), nullable=False)
    condition = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    mail = db.Column(db.String(30), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("User", back_populates="associated")
    quotas = db.relationship("Quota", back_populates="associates")
    discharge_date = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
