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


@app_views.route("/places_search", methods=["POST"])
def search():
    guide = request.get_json()
    if not guide:
        abort(400, "Not a JSON")

    state_ids = guide.get("states")
    city_ids = guide.get("cities")
    amenity_ids = guide.get("amenities")
    result = []

    if not guide and not state_ids and not city_ids:
        result = storage.all(Place)

    if state_ids:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        result.append(place)

    if city_ids:
        for city_id in city_ids:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in result:
                        result.append(place)

    if amenity_ids:
        for place in result:
            if place.amenities:
                place_amenity_ids = [amenity.id for amenity in place.amenities]
                for amenity_id in amenity_ids:
                    if amenity_id not in place_amenity_ids:
                        result.remove(place)
                        break

    result = [storage.get(Place, place.id).to_dict() for place in result]
    keys_to_remove = ["amenities", "reviews", "amenity_ids"]
    result = [
        {k: v for k, v in place_dict.items() if k not in keys_to_remove}
        for place_dict in result
    ]

    return jsonify(result)


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
