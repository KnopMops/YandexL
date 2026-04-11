import sqlalchemy as sa
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = "departments"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    chief_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    chief = orm.relationship("User", foreign_keys=[chief_id])
    members = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    user = orm.relationship("User", foreign_keys=[user_id])
