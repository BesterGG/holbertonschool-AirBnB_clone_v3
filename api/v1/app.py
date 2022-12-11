#!/usr/bin/python3
"""
    Comment
"""
from os import getenv
from api.v1.views.__init__ import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.errorhandler(404)
def not_found(exception):
    """ Handles 404 """
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def destroy(exception):
    """ Destroy session """
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(
        host='0.0.0.0' if host is None else host,
        port=5000 if port is None else port,
        threaded=True)
