from flask import make_response, jsonify
from flask_restful import reqparse, abort, Resource
import os
from data import db_session
from data.games import Game
from data.images import Image


def abort_if_game_not_found(game_id):
    session = db_session.create_session()
    game = session.query(Game).get(game_id)
    if not game:
        abort(404, message=f"Game {game_id} not found")


post_parser = reqparse.RequestParser()
post_parser.add_argument("title", required=True)
post_parser.add_argument("desc", required=True)
post_parser.add_argument("prev", required=True)
post_parser.add_argument("imgs", required=True)
post_parser.add_argument("file", required=True)
post_parser.add_argument("author", required=True, type=int)

put_parser = reqparse.RequestParser()
put_parser.add_argument("rate", required=True)


class GameResource(Resource):
    pass


class GameListResource(Resource):
    def get(self, author=None):
        session = db_session.create_session()
        if author is None:
            games = session.query(Game).all()
        else:
            games = session.query(Game).get(author)
        return jsonify(
            {
                'games':
                    [item.to_dict(only=("title", "prev", "author", "rate"))
                     for item in games]
            }
        )

    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        game = Game()
        game.title = args["title"]
        game.desc = args["desc"]
        game.author = args["author"]
        game.rate = 0.0
        game.votes = 0
        return jsonify({})
