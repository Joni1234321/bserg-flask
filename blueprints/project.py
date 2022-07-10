from bson import ObjectId
from flask import Blueprint, request
from pymongo.errors import WriteError

from globals import db
from util import jsonify, error, get_json

project = Blueprint("project", __name__)

def id_query(object_id):
    return {"_id": ObjectId(object_id)}


@project.route("/", methods=["GET"])
def get_projects():
    data = db.projects.find()
    return jsonify(list(data))


@project.route("/<string:object_id>", methods=["GET"])
def get_project(object_id):
    data = db.projects.find_one(id_query(object_id))
    try:
        return jsonify(data)
    except:
        error(422, f"project with id {object_id} does not exist")


@project.route("/<string:object_id>", methods=["DELETE"])
def delete_project(object_id):
    data = db.projects.delete_one(id_query(object_id))

    if data.raw_result['n'] == 0:
        error(422, f"could not delete project with id {object_id}")

    return f"successfully deleted object with id: {object_id}"


@project.route("/<string:object_id>", methods=["PUT"])
def update_project(object_id):
    json = get_json()
    del json["_id"]
    update = {"$set": json}

    data = db["projects"].update_one(id_query(object_id), update)
    if data.raw_result['n'] == 0:
        error(422, f"could not update project with id {object_id}")

    return f"successfully updated object with id: {object_id}"


@project.route("/", methods=["POST"])
def add_project():
    try:
        json = get_json()
        print(json)
        db.projects.insert_one(json)
        return "success"
    except WriteError:
        error(400, "Invalid insert")
