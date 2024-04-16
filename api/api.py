from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session

app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("db/games.db")
    app.run(host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
