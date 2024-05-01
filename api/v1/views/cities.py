#!/usr/bin/python3
""" handles all API actions for city object """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities")
def cities_in_a_state(state_id):
    """ Retrieves all city objects of a state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    result = []
    for city in state.cities:
        result.append(city.to_dict())

    return jsonify(result)


@app_views.route("/cities/<city_id>")
def city(city_id):
    """ Retrieve a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """ deletes a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """ Create a city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    city = City(state_id=state_id, **request.get_json())
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """ update city object using its id and put method"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    key = "name"
    setattr(city, key, request.get_json().get(key))
    city.save()

    return jsonify(city.to_dict())
