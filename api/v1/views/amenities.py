#!/usr/bin/python3
"""State API views"""
from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve the list of all amenities"""
    amenities_get = storage.all(Amenity).values()
    if amenities_get is None:
        abort(404)
    amenities_dict = []
    for amenity_get in amenities_get:
        all_amenities = amenity_get.to_dict()
        amenities_dict.append(all_amenities)

    return jsonify(amenities_dict)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                  strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a amenity object by ID"""
    amenity_get = storage.get(Amenity, amenity_id)
    if amenity_get is None:
        abort(404)
    return jsonify(amenity_get.to_dict())


@app_views.route(
        "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity object by ID"""
    amenity_delete = storage.get(Amenity, amenity_id)
    if amenity_delete is None:
        abort(404)
    storage.delete(amenity_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity object"""
    data = request.get_json()
    if data is None:
        abort(400, {"error": "Not a JSON"})

    if 'name' not in data:
        abort(400, {"error": "Missing name"})

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                  strict_slashes=False)
def update_amenity(amenity_id):
    """Update a amenity object"""
    amenity_get = storage.get(Amenity, amenity_id)
    if amenity_get is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, {"error": "Not a JSON"})

    for key, value in data.items():
        if key not in ['id', 'name', 'created_at', 'updated_at']:
            setattr(amenity_get, key, value)

    storage.save()
    return jsonify(amenity_get.to_dict()), 200
