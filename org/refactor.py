from globals import mil_db
from org.abbreviations import elongate_word
import json

def refactor_type (type):
    return " ".join([elongate_word(w) for w in type.split(" ")])

def refactor_org (org):
    stack = [org]
    while stack:
        current = stack.pop()
        current["type"] = refactor_type(current["type"]).replace(",","")
        if "children" in current:
            stack.extend(current["children"])

    return org

def refactor_all ():
    all_orgs = mil_db["org"].find()
    for org in all_orgs:
        ref_org = refactor_org(org)
        del ref_org["_id"]
        print(str(json.dumps(refactor_org(org)))[1:-1])
    return "HEJ"