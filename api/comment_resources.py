from flask import jsonify, request
from flask_restful import Resource, reqparse, abort
from tools import abort_if_game_not_found
from data import db_session
from data.comments import Comment
from data.games import Game


class CommentResource(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("mark", required=True, type=int)
        self.parser.add_argument("user", required=True, type=int)
        self.parser.add_argument("message", required=True)

    def put(self, game_id):
        abort_if_game_not_found(game_id)
        args = self.parser.parse_args()
        session = db_session.create_session()
        comment = session.query(Comment).filter(Comment.game_id == game_id, Comment.user == args["user"]).first()
        if comment is None:
            comment = Comment(game_id=game_id, user=args["user"])
            comment.mark = args["mark"]
            comment.message = args["message"]
            session.add(comment)
        else:
            comment.mark = args["mark"]
            comment.message = args["message"]
        game: Game = session.query(Game).get(game_id)
        game.update_rate()
        session.commit()
        return jsonify({"message": "ok"})

    @staticmethod
    def get(game_id):
        abort_if_game_not_found(game_id)
        user_id = request.args.get("user_id", None)
        if user_id is None:
            abort(400, message=f"User_id required")
        session = db_session.create_session()
        comment: Comment = session.query(Comment).filter(Comment.game_id == game_id, Comment.user == user_id).first()
        if comment is None:
            return jsonify({})
        return jsonify(comment.to_dict(only=["mark", "message"]))
