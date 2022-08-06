from json import dumps, loads

from flask import Blueprint, make_response, request

from globals import db, id_query

section = Blueprint("section", __name__)

sample_field = {"type": "text", "value": "lirum ipsum"}


@section.route("/<int:index>", methods=["POST"])
def create_section(object_id, index):
    try:
        section_json = loads(request.data)
    except:
        return make_response("Can't understand given json", 406)

    data = db.project_details.update_one(id_query(object_id),
                                         {"$set": {"sections." + str(index): section_json}},
                                         upsert=False)

    if data.matched_count == 0:
        return make_response(dumps(object_id), 404)

    # Object exists but is the same then
    if data.modified_count == 0:
        return make_response(dumps(object_id), 200)

    # If it modified an object
    return make_response(dumps(object_id), 200)
