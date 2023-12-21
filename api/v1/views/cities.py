#!/usr/bin/python3
"""State API views"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities_by_states(state_id):
    """Retrieve the list of all cities"""
    states_get = storage.get(State, state_id)
    if states_get is None:
        abort(404)
    cities_dict = []
    for city_get in states_get.cities:
        all_city = city_get.to_dict()
        cities_dict.append(all_city)
    return jsonify(cities_dict)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object by ID"""
    city_get = storage.get(City, city_id)
    if city_get is None:
        abort(404)
    return jsonify(city_get.to_dict())


@app_views.route(
        "/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by ID"""
    city_delete = storage.get(City, city_id)
    if city_delete is None:
        abort(404)
    storage.delete(city_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City object"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    city_get = storage.get(City, city_id)
    if city_get is None:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id','state_id', 'created_at', 'updated_at']:
            setattr(city_get, key, value)

    storage.save()
    return jsonify(city_get.to_dict()), 200
