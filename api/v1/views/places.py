#!/usr/bin/python3
""" handles all API actions for state object """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.user import User


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    """ Get all places in a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    result = []

    for place in city.places:
        result.append(place.to_dict())

    return jsonify(result)


@app_views.route("/places/<place_id>")
def place(place_id):
    """ Get a place by its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """ deletes a place by its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify(place.to_dict())


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """c reates a places in a city """
    data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if not storage.get(User, data["user_id"]):
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")

    place = Place(city_id=city_id, **data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """ updates a place by its id"""
    place = storage.get(Place, place_id)
    data = request.get_json()
    if not place:
        abort(404)
    if not data:
        abort(400, "Not a JSON")

    for key, value in place.to_dict().items():
        if key not in [
            "id",
            "user_id",
            "city_id",
            "created_at",
            "updated_at",
            "__class__",
        ]:
            setattr(place, key, data[key] if key in data else value)
    place.save()

    return jsonify(place.to_dict())
