from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
from sqlalchemy import desc
import os
import shutil
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
        self.parser.add_argument("rate", required=True, type=int)

    def get(self, game_id):
        abort_if_game_not_found(game_id)
        session = db_session.create_session()
        game: Game = session.query(Game).get(game_id)
        return jsonify(
            game.to_dict()
        )

    def delete(self, game_id):
        abort_if_game_not_found(game_id)
        session = db_session.create_session()
        game: Game = session.query(Game).get(game_id)
        for img in game.images:
            session.delete(img)
        shutil.rmtree(f"db/games/{game_id}")
        session.delete(game)
        session.commit()
        return jsonify({"message": "ok"})

    def put(self, game_id):
        abort_if_game_not_found(game_id)
        args = self.parser.parse_args()
        session = db_session.create_session()
        game: Game = session.query(Game).get(game_id)
        game.rate = round((game.rate * game.votes + args["rate"]) / (game.votes + 1), 1)
        game.votes += 1
        session.commit()
        return jsonify({"message": "ok"})


class GameListResource(Resource):
    def get(self):
        author = request.args.get("author", None)
        session = db_session.create_session()
        if author is None:
            games = session.query(Game).all()
        else:
            try:
                author = int(author)
            except ValueError:
                abort(400, message="Author value must be integer")
            games = session.query(Game).filter(Game.author == author)
        return jsonify(
            dict(games=[item.to_dict(only=("id", "title", "prev", "author", "rate")) for item in games])
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
        prev = self.load_file(args["prev"], f"db/games/{i}/preview")
        file = self.load_file(args["file"], f"db/games/{i}/file")
        for j in range(len(args["images"])):
            image = Image()
            image.game_id = i
            image.img = self.load_file(args["images"][j], f"db/games/{i}/images/{j}")
            session.add(image)

        game = Game()
        game.id = i
        game.title = args["title"]
        game.desc = args["desc"]
        game.author = args["author"]
        game.rate = 0.0
        game.votes = 0
        game.file = file
        game.prev = prev
        session.add(game)
        session.commit()
        return jsonify({"message": "ok"})

    def load_file(self, file: tuple[str, bytes], filename):
        fullname = f"{filename}.{file[0]}"
        with open(fullname, "wb") as f:
            f.write(file[1])
        return fullname
