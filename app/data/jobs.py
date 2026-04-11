import sqlalchemy as sa
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    team_leader_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    team_leader = orm.relationship("User", foreign_keys=[team_leader_id])
    work_size = sa.Column(sa.Integer, nullable=True)
    collaborators = sa.Column(sa.String, nullable=True)
    is_finished = sa.Column(sa.Boolean, default=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    user = orm.relationship("User", foreign_keys=[user_id])
