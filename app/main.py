import datetime
import os

from flask import Flask, abort, redirect, render_template, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from .data import db_session
from .data.departments import Department
from .data.jobs import Job
from .data.users import User
from .forms.department import DepartmentForm
from .forms.job import JobForm
from .forms.login import LoginForm
from .forms.register import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "sdfsdffdssdffds"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)

db_session.global_init("db/mars_one.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()

    return db_sess.get(User, user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()

    return render_template("index.html", jobs=jobs)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect("/login")

    return render_template("register.html", title="Регистрация", form=form)


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Job()

        job.title = form.title.data
        job.team_leader_id = form.team_leader_id.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.user_id = current_user.id

        db_sess.add(job)
        db_sess.commit()

        return redirect("/")

    return render_template("add_job.html", title="Adding a Job", form=form)


@app.route("/edit_job/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):
    form = JobForm()

    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == id).first()

    if not job:
        abort(404)

    if job.user_id != current_user.id and current_user.id != 1:
        abort(403)

    if request.method == "GET":
        form.title.data = job.title
        form.team_leader_id.data = job.team_leader_id
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished

    if form.validate_on_submit():
        job.title = form.title.data
        job.team_leader_id = form.team_leader_id.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        db_sess.commit()

        return redirect("/")

    return render_template("add_job.html", title="Редактирование работы", form=form)


@app.route("/delete_job/<int:id>", methods=["GET", "POST"])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == id).first()

    if not job:
        abort(404)

    if job.user_id != current_user.id and current_user.id != 1:
        abort(403)

    db_sess.delete(job)
    db_sess.commit()

    return redirect("/")


@app.route("/departments")
def departments():
    db_sess = db_session.create_session()
    depts = db_sess.query(Department).all()
    return render_template("departments.html", departments=depts)


@app.route("/add_department", methods=["GET", "POST"])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dept = Department()
        dept.title = form.title.data
        dept.chief_id = form.chief_id.data
        dept.members = form.members.data
        dept.email = form.email.data
        dept.user_id = current_user.id
        db_sess.add(dept)
        db_sess.commit()
        return redirect("/departments")
    return render_template("department_form.html", title="Add a Department", form=form)


@app.route("/edit_department/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).filter(Department.id == id).first()
    if not dept:
        abort(404)
    if dept.user_id != current_user.id and current_user.id != 1:
        abort(403)

    if request.method == "GET":
        form.title.data = dept.title
        form.chief_id.data = dept.chief_id
        form.members.data = dept.members
        form.email.data = dept.email

    if form.validate_on_submit():
        dept.title = form.title.data
        dept.chief_id = form.chief_id.data
        dept.members = form.members.data
        dept.email = form.email.data
        db_sess.commit()
        return redirect("/departments")
    return render_template("department_form.html", title="Edit Department", form=form)


@app.route("/delete_department/<int:id>", methods=["GET", "POST"])
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).filter(Department.id == id).first()
    if not dept:
        abort(404)
    if dept.user_id != current_user.id and current_user.id != 1:
        abort(403)
    db_sess.delete(dept)
    db_sess.commit()
    return redirect("/departments")


if __name__ == "__main__":
    if not os.path.exists("db"):
        os.makedirs("db")

    app.run(port=8080, host="127.0.0.1", debug=True)
