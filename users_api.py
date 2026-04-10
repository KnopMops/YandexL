from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User

blueprint = Blueprint("users_api", __name__, template_folder="templates")


def user_to_dict(user):
    return user.to_dict(
        only=(
            "id",
            "surname",
            "name",
            "age",
            "position",
            "speciality",
            "address",
            "email",
            "modified_date",
            "city_from",
        )
    )


@blueprint.route("/api/users", methods=["GET"])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    return jsonify({"users": [user_to_dict(u) for u in users]})


@blueprint.route("/api/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    return jsonify({"user": user_to_dict(user)})


@blueprint.route("/api/users", methods=["POST"])
def create_user():
    required_fields = [
        "surname",
        "name",
        "age",
        "position",
        "speciality",
        "address",
        "email",
        "password",
    ]
    missing = [f for f in required_fields if f not in request.json]

    db_sess = db_session.create_session()

    user = User(
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json["position"],
        speciality=request.json["speciality"],
        address=request.json["address"],
        email=request.json["email"],
        city_from=request.json.get("city_from"),
    )
    user.hashed_password = generate_password_hash(request.json["password"])

    db_sess.add(user)
    db_sess.commit()


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    updatable_fields = [
        "surname",
        "name",
        "age",
        "position",
        "speciality",
        "address",
        "email",
        "password",
        "city_from",
    ]

    for field in updatable_fields:
        if field in request.json:
            value = request.json[field]
            if field == "password":
                user.hashed_password = generate_password_hash(value)
            elif field == "email":
                if value != user.email:
                    existing = db_sess.query(User).filter(User.email == value).first()
                    if existing:
                        return make_response(
                            jsonify({"error": "Email already in use"}), 400
                        )
                    user.email = value
            else:
                setattr(user, field, value)

    db_sess.commit()


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    db_sess.delete(user)
    db_sess.commit()
