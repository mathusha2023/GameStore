from flask import send_file, request
from flask_restful import abort, Resource
import os


class GetFileResource(Resource):
    def get(self):
        path = request.args.get("filepath", None)
        if path is None:
            abort(400, message="Filepath argument required!")
        if not os.path.isfile(path):
            abort(404, message=f"File {path} not found")
        return send_file(path)
