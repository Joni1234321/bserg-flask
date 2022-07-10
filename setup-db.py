from globals import db

def setup ():
    db["projects"].create_index("url", unique=True)

setup()