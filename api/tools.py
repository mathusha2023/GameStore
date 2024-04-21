from flask_restful import abort
from data import db_session
from data.games import Game


def abort_if_game_not_found(game_id):
    session = db_session.create_session()
    game = session.query(Game).get(game_id)
    if not game:
        abort(404, message=f"Game {game_id} not found")


def load_file(file: tuple[str, bytes], filename):
    fullname = f"{filename}.{file[0]}"
    with open(fullname, "wb") as f:
        f.write(file[1])
    return fullname


def check_args(args):
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
