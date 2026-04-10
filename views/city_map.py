import requests
from flask import Blueprint, jsonify, make_response, render_template

city_blueprint = Blueprint("city_map", __name__, template_folder="templates")


@city_blueprint.route("/users_show/<int:user_id>")
def show_city(user_id):
    response = requests.get(f"http://127.0.0.1:5000/api/users/{user_id}")

    user_data = response.json()["user"]

    name = user_data["name"]
    surname = user_data["surname"]
    city = user_data.get("city_from")

    if not city:
        city = "Москва"

    YANDEX_MAPS_API_KEY = ""

    return render_template(
        "city_map.html",
        name=name,
        surname=surname,
        city=city,
        api_key=YANDEX_MAPS_API_KEY,
    )
