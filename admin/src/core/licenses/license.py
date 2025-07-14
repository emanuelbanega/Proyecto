from datetime import datetime
from src.core.database import db

class License(db.Model):

    __tablename__ = "licenses"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    associated_id = db.Column(db.Integer, db.ForeignKey("associates.id"))
    associated = db.relationship("Associated", backref="credential")
    photo = db.Column(db.String(30), nullable=False)
    qr = db.Column(db.String(30), nullable=False)
    discharge_date = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False )