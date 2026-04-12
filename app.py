from flask import Flask
from flask_restful import Api

import jobs_resources
import users_resources
from data import db_session

app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("data/db/blogs.sqlite")
    # Регистрация ресурсов
    api.add_resource(users_resources.UsersListResource, "/api/v2/users")
    api.add_resource(users_resources.UsersResource, "/api/v2/users/<int:user_id>")
    api.add_resource(jobs_resources.JobsListResource, "/api/v2/jobs")
    api.add_resource(jobs_resources.JobsResource, "/api/v2/jobs/<int:job_id>")
    app.run(port=5000, host="127.0.0.1")


if __name__ == "__main__":
    main()
