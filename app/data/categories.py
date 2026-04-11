import sqlalchemy as sa
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase

association_table = sa.Table(
    "job_to_category",
    SqlAlchemyBase.metadata,
    sa.Column("job_id", sa.Integer, sa.ForeignKey("jobs.id")),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
)


class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
