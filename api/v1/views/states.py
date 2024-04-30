#!/usr/bin/python3
""" handles all API actions for state object"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states")
def states():
    """Retrieve all State objects"""
    objects = []
    for value in storage.all(State).values():
        objects.append(value.to_dict())
    return jsonify(objects)


@app_views.route("/states/<state_id>")
def state(state_id: str):
    """Dynamic Routing for states by its id"""
    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """ delete a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    """creates a state object"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    state = State(**request.get_json())
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """ Updates state object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    key = "name"
    setattr(state, key, request.get_json().get(key))
    state.save()
    return jsonify(state.to_dict())
