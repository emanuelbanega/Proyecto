from datetime import datetime

from src.core.database import db

associates_sports = db.Table(
    "associates_sports",
    db.Column(
        "associate_id", db.Integer, db.ForeignKey("associates.id"), primary_key=True
    ),
    db.Column("sport_id", db.Integer, db.ForeignKey("sports.id"), primary_key=True),
)


class Sport(db.Model):

    __tablename__ = "sports"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(50), nullable=False)
    instructors_names = db.Column(db.String(300), nullable=False)
    schedule = db.Column(db.String(300), nullable=False)
    monthly_fee = db.Column(db.String(10), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)
    associates = db.relationship(
        "Associated", secondary=associates_sports, backref="sports"
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
