import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

from models import Base, Jobs, User

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"  # необходим для flash-сообщений

engine = create_engine("sqlite:///mars_explorer.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route("/")
def jobs_list():
    session = Session()
    all_jobs = session.query(Jobs).options(joinedload(Jobs.leader)).all()
    session.close()

    return render_template("index.html", jobs=all_jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        surname = request.form.get("surname", "").strip()
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        position = request.form.get("position", "").strip()
        speciality = request.form.get("speciality", "").strip()
        address = request.form.get("address", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if not surname:
            errors.append("Фамилия обязательна")
        if not name:
            errors.append("Имя обязательно")
        if not age_str or not age_str.isdigit() or int(age_str) <= 0:
            errors.append("Возраст должен быть положительным числом")
        else:
            age = int(age_str)
        if not position:
            errors.append("Должность обязательна")
        if not speciality:
            errors.append("Профессия обязательна")
        if not address:
            errors.append("Адрес обязателен")
        if not email:
            errors.append("Email обязателен")
        if not password:
            errors.append("Пароль обязателен")
        if password != confirm:
            errors.append("Пароли не совпадают")

        if not errors:
            session = Session()
            if User.email_exists(session, email):
                errors.append("Пользователь с таким email уже зарегистрирован")
            else:
                user = User(
                    surname=surname,
                    name=name,
                    age=age,
                    position=position,
                    speciality=speciality,
                    address=address,
                    email=email,
                    modified_date=datetime.datetime.now(),
                )

                user.set_password(password)
                session.add(user)
                session.commit()
                session.close()
                flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")

                return redirect(url_for("jobs_list"))

            session.close()

        for error in errors:
            flash(error, "danger")

        return render_template("register.html")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
