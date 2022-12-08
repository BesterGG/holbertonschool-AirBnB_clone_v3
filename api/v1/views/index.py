#!/usr/bin/python3
"""

"""
from flask import jsonify
from api.v1.views.__init__ import app_views

@app_views.route('/status')
def status():
    """
        Returns API status
    """
    return jsonify({"status": "OK"})
