import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True
    )
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = orm.relationship("User")

    def to_dict(self, only=None):
        if only is None:
            return {
                "id": self.id,
                "team_leader": self.team_leader,
                "job": self.job,
                "work_size": self.work_size,
                "collaborators": self.collaborators,
                "start_date": self.start_date.isoformat() if self.start_date else None,
                "end_date": self.end_date.isoformat() if self.end_date else None,
                "is_finished": self.is_finished,
            }
        else:
            d = {}
            for key in only:
                if hasattr(self, key):
                    value = getattr(self, key)
                    if key in ("start_date", "end_date") and value:
                        value = value.isoformat()
                    d[key] = value
            return d
