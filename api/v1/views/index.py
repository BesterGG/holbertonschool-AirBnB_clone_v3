#!/usr/bin/python3
"""

"""
from flask import jsonify
from api.v1.views.__init__ import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
        Returns API status
    """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def api_stats():
    """
        Returns API stats for analytics
    """
    return jsonify(
        {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        }
    )
