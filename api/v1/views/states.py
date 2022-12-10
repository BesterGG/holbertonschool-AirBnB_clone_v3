#!/usr/bin/python3
"""
    Comment
"""
from api.v1.views.__init__ import app_views
from models.__init__ import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'])
def states():
    """returns"""
    st = storage.all('State')
    list = []
    for k, v in st.items():
        list.append(v.to_dict())
    return jsonify(list)

@app_views.route('/states/<state_id>', methods=['GET'])
def state_id(state_id):
    """Get the state"""
    from models.state import State
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    else:
        return jsonify(st.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """Delete"""
    from models.state import State
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    else:
        storage.delete(State)
        storage.save()
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def post_state():
    """Comment"""
    import json
    from models.state import State
    dic_t = request.get_json()
    if dic_t is None or type(dic_t) != dict:   
        abort(400, description='Not a JSON')
    elif 'name' not in dic_t.keys():
        abort(400, description='Missing name')
    else:
        newstate = State(**dic_t)
        newstate.save()
        return jsonify(newstate.to_dict()), 201