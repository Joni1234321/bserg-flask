from flask import Flask
from flask_cors import CORS
from blueprints.project import project
from blueprints.section import section


def create_url(url):
    return "/api/v1" + url


app = Flask(__name__)
CORS(app)

app.register_blueprint(project, url_prefix=create_url("/project"))
app.register_blueprint(section, url_prefix=create_url("/project/<string:object_id>/section"))


@app.route(create_url("/"))
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
