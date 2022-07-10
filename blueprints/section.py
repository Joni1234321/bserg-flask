from flask import Blueprint

section = Blueprint("section", __name__)


@section.route("/<int:index>/field", methods=["POST"])
def add_field(object_id, index):
    print("adding field")
    print(f"{object_id} - {index}")
    return ""
