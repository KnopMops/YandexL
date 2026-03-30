from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

from models import Base, Jobs, User

app = Flask(__name__)

engine = create_engine("sqlite:///mars_explorer.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route("/")
@app.route("/jobs")
def jobs_list():
    session = Session()
    all_jobs = session.query(Jobs).options(joinedload(Jobs.leader)).all()
    session.close()
    return render_template("jobs.html", jobs=all_jobs)


if __name__ == "__main__":
    app.run(debug=True)
