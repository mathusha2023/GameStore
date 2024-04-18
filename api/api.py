from flask import Flask, url_for
from flask_restful import Api
import os
from data import db_session
from game_resources import GameResource, GameListResource

app = Flask(__name__)
app.config["SECRET_KEY"] = "IfYoUhAvErEaDtHiSyOuArEgEy"

api = Api(app)
api.add_resource(GameResource, "/game/<int:game_id>")
api.add_resource(GameListResource, "/games", "/games/<int:author_id>")


def main():
    if not os.path.isdir("db"):
        os.mkdir("db")
    if not os.path.isdir("static"):
        os.mkdir("static")
        os.mkdir("static/games")
    db_session.global_init("db/games.db")
    app.run(host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
