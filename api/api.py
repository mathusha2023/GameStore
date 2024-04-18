from flask import Flask
from flask_restful import Api
import os
from data import db_session
from game_resources import GameResource, GameListResource
from get_file_resource import GetFileResource

app = Flask(__name__)
app.config["SECRET_KEY"] = "IfYoUhAvErEaDtHiSyOuArEgEy"

api = Api(app)
api.add_resource(GameResource, "/game/<int:game_id>")
api.add_resource(GameListResource, "/games")
api.add_resource(GetFileResource, "/file")


def main():
    if not os.path.isdir("db"):
        os.mkdir("db")
        os.mkdir("db/games")
    db_session.global_init("db/games.db")
    app.run(host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
