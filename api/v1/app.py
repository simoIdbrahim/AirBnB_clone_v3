#!/usr/bin/python3
""" run flask app"""

from api.v1.views import app_views
import os
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask('__name__')
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

if os.getenv("HBNB_API_HOST"):
    HOST = os.getenv("HBNB_API_HOST")
else:
    HOST = '0.0.0.0'

if os.getenv("HBNB_API_HOST"):
    PORT = os.getenv("HBNB_API_PORT")
else:
    PORT = 5000


@app.errorhandler(404)
def notFound(err):
    """ err not found err """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception=None):
    """ end database """
    storage.close()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
