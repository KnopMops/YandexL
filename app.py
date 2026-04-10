from flask import Flask
from views.city_map import city_blueprint

from data import db_session
from users_api import blueprint as users_api_blueprint

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(users_api_blueprint)
    app.register_blueprint(city_blueprint)
    app.run(debug=True)


if __name__ == "__main__":
    main()
