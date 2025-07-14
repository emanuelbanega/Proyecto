from datetime import datetime

from src.core.database import db


class Permission(db.Model):

    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
