#!/usr/bin/python3
"""State API views"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve the list of all objects"""
    states_get = storage.all(State).values()
    state_dict = []
    for state_get in states_get:
        all_states = state_get.to_dict()
        state_dict.append(all_states)
    return jsonify(state_dict)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieve a State object by ID"""
    state_get = storage.get(State, state_id)
    if state_get is None:
        abort(404)
    return jsonify(state_get.to_dict())


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object by ID"""
    state_delete = storage.get(State, state_id)
    if state_delete is None:
        abort(404)
    storage.delete(state_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State object"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    state_get = storage.get(State, state_id)
    if state_get is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_get, key, value)

    storage.save()
    return jsonify(state_get.to_dict()), 200
