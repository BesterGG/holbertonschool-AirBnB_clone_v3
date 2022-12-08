#!/usr/bin/python3
import json
from api.v1.views import app_views

@app_views.route('/status')
def status():
    return json.dump({"status": "OK"})
