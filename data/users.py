import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    jobs = orm.relationship("Jobs", back_populates='user')

    def to_dict(self, only=None):
        if only is None:
            return {
                'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'age': self.age,
                'address': self.address,
                'email': self.email,
                'position': self.position,
                'speciality': self.speciality,
                'hashed_password': self.hashed_password,
                'modified_date': self.modified_date.isoformat() if self.modified_date else None
            }
        else:
            d = {}
            for key in only:
                if hasattr(self, key):
                    value = getattr(self, key)
                    if key == 'modified_date' and value:
                        value = value.isoformat()
                    d[key] = value
            return d
