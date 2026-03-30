from data import db_session
from flask import Flask
from flask_restful import Api
from jobs_resource import JobsListResource, JobsResource
from users_resource import UsersListResource, UsersResource

app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("db/blogs.db")
    api.add_resource(UsersListResource, "/api/users")
    api.add_resource(UsersResource, "/api/users/<int:user_id>")
    api.add_resource(JobsListResource, "/api/jobs")
    api.add_resource(JobsResource, "/api/jobs/<int:job_id>")
    app.run(debug=True)


if __name__ == "__main__":
    main()
