from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
import os
from data import db_session
from game_resources import GameResource, GameListResource
from get_file_resource import GetFileResource
from comment_resources import CommentResource

load_dotenv()
HOST = os.getenv('API_HOST')
PORT = os.getenv('API_PORT')
SECRET_KEY = os.getenv('API_SECRET_KEY')


class MyApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config["SECRET_KEY"] = SECRET_KEY
        self.api = Api(self)
        self.api.add_resource(GameResource, "/game/<int:game_id>")
        self.api.add_resource(GameListResource, "/games")
        self.api.add_resource(CommentResource, "/comment/<int:game_id>")
        self.api.add_resource(GetFileResource, "/file")

    def run(self):
        super().run(host=HOST, port=PORT)


def main():
    if not os.path.isdir("db"):
        os.mkdir("db")
        os.mkdir("db/games")
    db_session.global_init("db/games.db")
    app = MyApp()
    app.run()


if __name__ == "__main__":
    main()
