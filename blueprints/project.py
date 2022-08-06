from flask import Blueprint, request, make_response
from pymongo.errors import WriteError
from flask.json import loads
from bson.json_util import dumps

from globals import db, id_query

project = Blueprint("project", __name__)

@project.route("/", methods=["GET"])
def get_projects():
    data = db.projects.find()
    return make_response(dumps(list(data)), 200)


@project.route("/<string:object_id>", methods=["GET"])
def get_project(object_id):
    p = db.projects.find_one(id_query(object_id))

    if p is None:
        return make_response(dumps(object_id), 404)

    details = db.project_details.find_one(id_query(object_id))
    if details is None:
        details = {"_id": p["_id"], "schema_version": 1}
        re = db.project_details.insert_one(details)
        if not re.acknowledged:
            return make_response(f"not acknowledged", 400)

    p["details"] = details

    try:
        return make_response(dumps(p), 200)
    except WriteError as e:
        return make_response(f"{e}", 400)
    except Exception as e:
        print(e)
        return make_response(f"unhandled error: {e}", 400)


@project.route("/<string:object_id>", methods=["DELETE"])
def delete_project(object_id):
    # delete project
    data = db.projects.delete_one(id_query(object_id))

    if data.raw_result['n'] == 0:
        return make_response(f"could not delete project with id {object_id}", 400)

    # delete details
    db.project_details.delete_one(id_query(object_id))

    return make_response(dumps(object_id), 204)


@project.route("/<string:object_id>", methods=["PUT"])
def update_project(object_id):
    json = loads(request.data)
    del json["_id"]
    update = {"$set": json}
    data = db["projects"].update_one(id_query(object_id), update)

    # Object does not exist
    if data.matched_count == 0:
        return make_response(dumps(object_id), 404)

    # Object exists but is the same then
    if data.modified_count == 0:
        return make_response(dumps(object_id), 200)

    # If it modified an object
    return make_response(dumps(object_id), 200)


@project.route("/", methods=["POST"])
def add_project():
    try:
        json = loads(request.data)
    except:
        return make_response("Can't understand given json", 406)

    try:
        re = db.projects.insert_one(json)
        # return id of inserted object
        return make_response(dumps(re.inserted_id), 201)
    except WriteError:
        return make_response("Invalid insert", 400)
