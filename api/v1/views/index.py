#!/usr/bin/python3
""" index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}

@app_views.route("/status", methods=["GET"])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=["GET"])
def stats():
    """get objects count"""
    count_data = {}
    for key, val in classes:
        count_data[key] = storage.count(val)

    return jsonify(count_data)
