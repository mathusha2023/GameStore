from flask import send_file, request
from flask_restful import abort, Resource
import os


class GetFileResource(Resource):

    @staticmethod
    def get():
        path = request.args.get("p", None)
        if path is None:
            abort(400, message="Filepath argument required!")
        check_path = path.replace("\\", "/").split("/")
        if len(check_path) < 2:
            abort(404, message=f"File {path} not found")
        if check_path[0] != "db" or check_path[1] != "games":
            abort(403, message=f"Access to the file {path} is prohibited")
        if not os.path.isfile(path):
            abort(404, message=f"File {path} not found")
        return send_file(path)
