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
