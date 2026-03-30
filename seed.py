import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Jobs, User


def seed_database():
    engine = create_engine("sqlite:///mars_explorer.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(User).count() == 0:
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

        colonists = [
            User(
                surname="Armstrong",
                name="Neil",
                age=35,
                position="engineer",
                speciality="mechanical engineer",
                address="module_2",
                email="neil.armstrong@mars.org",
                hashed_password="neil123",
                modified_date=datetime.datetime.now(),
            ),
            User(
                surname="Aldrin",
                name="Buzz",
                age=38,
                position="pilot",
                speciality="flight engineer",
                address="module_3",
                email="buzz.aldrin@mars.org",
                hashed_password="buzz456",
                modified_date=datetime.datetime.now(),
            ),
            User(
                surname="Collins",
                name="Michael",
                age=42,
                position="scientist",
                speciality="geologist",
                address="module_1",
                email="michael.collins@mars.org",
                hashed_password="mike789",
                modified_date=datetime.datetime.now(),
            ),
        ]
        session.add_all(colonists)
        session.commit()
        print("Добавлены пользователи (капитан и 3 колониста).")

    if session.query(Jobs).count() == 0:
        captain_id = session.query(User.id).filter(User.surname == "Scott").scalar()
        if captain_id:
            job = Jobs(
                team_leader=captain_id,
                job="deployment of residential modules 1 and 2",
                work_size=15,
                collaborators="2, 3",
                start_date=datetime.datetime.now(),
                is_finished=False,
            )
            session.add(job)
            session.commit()
            print("Добавлена работа для развертывания модулей.")
        else:
            print("Капитан не найден, работа не добавлена.")
    else:
        print("В таблице jobs уже есть данные, пропускаем.")

    session.close()


if __name__ == "__main__":
    seed_database()
