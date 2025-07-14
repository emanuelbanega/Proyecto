from datetime import datetime

from src.core.database import db


role_permission = db.Table(
    "role_permission",
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)


class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    permission = db.relationship("Permission", secondary=role_permission)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)


def rol_tiene_permiso(role, namePermission):
    """Recorre los permisos del rol, devuelve True si encuentra 'namePermission'"""

    for permiso in role.permission:
        if permiso.name == namePermission:
            return True
    return False
