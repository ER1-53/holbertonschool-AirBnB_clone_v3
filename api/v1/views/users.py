#!/usr/bin/python3
"""State API views"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve the list of all users"""
    user_get = storage.all(User).values()
    if user_get is None:
        abort(404)
    users_dict = []
    for user_get in user_get:
        all_users = user_get.to_dict()
        users_dict.append(all_users)

    return jsonify(users_dict)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user object by ID"""
    user_get = storage.get(User, user_id)
    if user_get is None:
        abort(404)
    return jsonify(user_get.to_dict())


@app_views.route(
        "/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Delete a user object by ID"""
    user_delete = storage.get(User, user_id)
    if user_delete is None:
        abort(404)
    storage.delete(user_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user object"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if 'password' not in data:
        abort(400, "Missing password")
    if 'email' not in data:
        abort(400, "Missing email")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a user object"""
    user_get = storage.get(User, user_id)
    if user_get is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'name', 'created_at', 'updated_at']:
            setattr(user_get, key, value)

    storage.save()
    return jsonify(user_get.to_dict()), 200
