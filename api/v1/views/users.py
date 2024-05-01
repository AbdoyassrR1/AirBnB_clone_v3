#!/usr/bin/python3
""" handles all API actions for user object """
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import request, abort, jsonify
from models.engine.db_storage import classes


@app_views.route("/users")
def users():
    """get all users"""
    users = storage.all(User)
    result = []
    for user in users.values():
        result.append(user.to_dict())

    return jsonify(result)


@app_views.route("/users/<user_id>")
def one_user(user_id):
    """ get one user by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """ Deletes a user by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()

    return jsonify({})


@app_views.route("/users", methods=["POST"])
def create_user():
    """ creates user """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")

    user = User(**request.get_json())
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """ updates an existing user by its id"""
    user = storage.get(classes["User"], user_id)
    if user is None:
        abort(404)

    user_data = request.get_json(force=True, silent=True)
    if type(user_data) is not dict:
        abort(400, "Not a JSON")

    for key, value in user_data.items():
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict())
