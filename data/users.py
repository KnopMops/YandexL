import datetime

import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    city_from = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self, only=None):
        data = {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "age": self.age,
            "position": self.position,
            "speciality": self.speciality,
            "address": self.address,
            "email": self.email,
            "modified_date": self.modified_date.isoformat()
            if self.modified_date
            else None,
            "city_from": self.city_from,
        }
        if only:
            return {k: v for k, v in data.items() if k in only}
        return data
