from bson.json_util import dumps
from flask import abort, make_response, request
from flask.json import loads


def jsonify(data):
    return dumps(data)


def get_json():
    return loads(request.data)


def error(error_code, message):
    abort(make_response(jsonify({"error", message}), error_code))
