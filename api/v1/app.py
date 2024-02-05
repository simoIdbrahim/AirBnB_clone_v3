#!/usr/bin/python3
""" flask app """


from api.v1.views import app_views
from os import getenv
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask import jsonify

app = Flask('__name__')
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def notFound(err):
    """ 404 err code status"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception=None):
    """ end database"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=host, debug=True, threaded=True)
