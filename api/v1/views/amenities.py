#!/usr/bin/python3
""" handles all API actions for amenity  object """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import request, abort, jsonify


@app_views.route("/amenities")
def amenities():
    """ retrieves list of all `Amenity` objects """
    amenities = storage.all(Amenity)
    result = []
    for amenity in amenities.values():
        result.append(amenity.to_dict())

    return jsonify(result)


@app_views.route("/amenities/<amenity_id>")
def amenity(amenity_id):
    """ Retrieve one amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """ Deletes an amenity by its id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """ Create an amenity """
    if not request.get_json():
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    amenity = Amenity(**request.get_json())
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """ Update an existing amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    payload = request.get_json()
    if not amenity:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    key = "name"
    setattr(amenity, key, payload[key])
    amenity.save()

    return jsonify(amenity.to_dict()), 200
