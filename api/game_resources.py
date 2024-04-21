from flask import jsonify, request
from flask_restful import abort, Resource
from sqlalchemy import desc
import os
import shutil
import pickle
from data import db_session
from data.games import Game
from data.images import Image
from tools import abort_if_game_not_found, load_file


class GameResource(Resource):
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
        self.check_args(args)
        session = db_session.create_session()
        sp = session.query(Game).order_by(desc(Game.id)).limit(1).all()
        if not sp:
            i = 1
        else:
            i = sp[0].id + 1

        os.mkdir(f"db/games/{i}")
        os.mkdir(f"db/games/{i}/images")
        prev = load_file(args["prev"], f"db/games/{i}/preview")
        file = load_file(args["file"], f"db/games/{i}/file")
        for j in range(len(args["images"])):
            image = Image()
            image.game_id = i
            image.img = load_file(args["images"][j], f"db/games/{i}/images/{j}")
            session.add(image)

        game = Game()
        game.id = i
        game.title = args["title"]
        game.desc = args["desc"]
        game.author = args["author"]
        game.rate = 0.0
        game.file = file
        game.prev = prev
        session.add(game)
        session.commit()
        return jsonify({"message": "ok"})

    def check_args(self, args):
        s = args.get("title", None)
        if s is None or not isinstance(s, str):
            abort(400, message="Incorrect arg title")

        s = args.get("desc", None)
        if s is None or not isinstance(s, str):
            abort(400, message="Incorrect arg desc")

        s = args.get("author", None)
        if s is None or not isinstance(s, int):
            abort(400, message="Incorrect arg author")

        s = args.get("prev", None)
        if s is None or not isinstance(s, (tuple, list)) or len(s) != 2 or not isinstance(s[0], str) or not isinstance(
                s[1], bytes):
            abort(400, message="Incorrect arg prev")

        s = args.get("file", None)
        if s is None or not isinstance(s, (tuple, list)) or len(s) != 2 or not isinstance(s[0], str) or not isinstance(
                s[1], bytes):
            abort(400, message="Incorrect arg file")

        s = args.get("images", None)
        if s is None or not isinstance(s, (tuple, list)):
            abort(400, message="Incorrect arg images")
        for i in s:
            if not isinstance(i, (tuple, list)) or len(i) != 2 or not isinstance(i[0], str) or not isinstance(i[1],
                                                                                                              bytes):
                abort(400, message="Incorrect arg images")
