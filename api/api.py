from flask import Flask
from flask_restful import Api
import os
from data import db_session
from game_resources import GameResource, GameListResource
from get_file_resource import GetFileResource
from comment_resources import CommentResource


class MyApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config["SECRET_KEY"] = "IfYoUhAvErEaDtHiSyOuArEgEy"
        self.api = Api(self)
        self.api.add_resource(GameResource, "/game/<int:game_id>")
        self.api.add_resource(GameListResource, "/games")
        self.api.add_resource(CommentResource, "/comment/<int:game_id>")
        self.api.add_resource(GetFileResource, "/file")

    def run(self):
        super().run(host="127.0.0.1", port=8080)


def main():
    if not os.path.isdir("db"):
        os.mkdir("db")
        os.mkdir("db/games")
    db_session.global_init("db/games.db")
    app = MyApp()
    app.run()


if __name__ == "__main__":
    main()
