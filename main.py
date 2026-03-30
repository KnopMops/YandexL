import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conn import SqlAlchemyBase

# from jobs import Jobs
from users import User


def main():
    engine = create_engine("sqlite:///mars_explorer.db")
    SqlAlchemyBase.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    captain = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="scott_chief@mars.org",
        hashed_password="cap",
        modified_date=datetime.datetime.now(),
    )

    session.add(captain)

    colonist1 = User(
        surname="Armstrong",
        name="Neil",
        age=35,
        position="engineer",
        speciality="mechanical engineer",
        address="module_2",
        email="neil.armstrong@mars.org",
        hashed_password="neil123",
        modified_date=datetime.datetime.now(),
    )

    session.add(colonist1)

    colonist2 = User(
        surname="Aldrin",
        name="Buzz",
        age=38,
        position="pilot",
        speciality="flight engineer",
        address="module_3",
        email="buzz.aldrin@mars.org",
        hashed_password="buzz456",
        modified_date=datetime.datetime.now(),
    )

    session.add(colonist2)

    colonist3 = User(
        surname="Collins",
        name="Michael",
        age=42,
        position="scientist",
        speciality="geologist",
        address="module_1",
        email="michael.collins@mars.org",
        hashed_password="mike789",
        modified_date=datetime.datetime.now(),
    )

    session.add(colonist3)

    session.commit()
    session.close()


if __name__ == "__main__":
    main()
