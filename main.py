import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conn import SqlAlchemyBase
from jobs import Jobs
from users import User


def main():
    engine = create_engine("sqlite:///mars_explorer.db")
    SqlAlchemyBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.datetime.now()
    job.is_finished = False

    session.add(job)
    session.commit()

    session.close()


if __name__ == "__main__":
    main()
