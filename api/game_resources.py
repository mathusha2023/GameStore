from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
from sqlalchemy import desc
import os
import pickle
from data import db_session
from data.games import Game
from data.images import Image


def abort_if_game_not_found(game_id):
    session = db_session.create_session()
    game = session.query(Game).get(game_id)
    if not game:
        abort(404, message=f"Game {game_id} not found")


class GameResource(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("rate", required=True)


class GameListResource(Resource):
    def get(self, author=None):
        session = db_session.create_session()
        if author is None:
            games = session.query(Game).all()
        else:
            games = session.query(Game).get(author)
        return jsonify(
            dict(games=[item.to_dict(only=("title", "prev", "author", "rate")) for item in games])
        )

    def post(self):
        args = pickle.loads(request.data)
        session = db_session.create_session()
        sp = session.query(Game).order_by(desc(Game.id)).limit(1).all()
        if not sp:
            i = 1
        else:
            i = sp[0].id + 1

        os.mkdir(f"db/games/{i}")
        os.mkdir(f"db/games/{i}/images")
        self.load_file(args["prev"], f"db/games/{i}/preview")
        self.load_file(args["file"], f"db/games/{i}/file")
        for j in range(len(args["images"])):
            self.load_file(args["images"][j], f"db/games/{i}/images/{j}")

        game = Game()
        game.id = i
        game.title = args["title"]
        game.desc = args["desc"]
        game.author = args["author"]
        game.rate = 0.0
        game.votes = 0
        game.file = "A"
        game.prev = "as"
        session.add(game)
        session.commit()
        return jsonify({})

    def load_file(self, file: tuple[str, bytes], filename):
        with open(f"{filename}.{file[0]}", "wb") as f:
            f.write(file[1])
