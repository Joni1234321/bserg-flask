from bson.json_util import dumps

from flask import Blueprint, make_response
from pymongo.errors import WriteError

from globals import db, id_query, mil_db

mil = Blueprint("mil", __name__)


@mil.route("/", methods=["GET"])
def get_orgs():
    data = mil_db["org"].find()
    return make_response(dumps(list(data)), 200)


@mil.route("/<string:object_id>", methods=["GET"])
def get_org(object_id):
    org = mil_db["org"].find_one(id_query(object_id))
    if org is None:
        return make_response(dumps(object_id), 404)

    try:
        return make_response(dumps(org), 200)
    except WriteError as e:
        return make_response(f"{e}", 400)
    except Exception as e:
        print(e)
        return make_response(f"unhandled error: {e}", 400)
