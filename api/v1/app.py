#!/usr/bin/python3
"""
    Comment
"""
from os import getenv
from api.v1.views.__init__ import app_views
from flask import Flask, render_template
from jinja2 import TemplateNotFound
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


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
