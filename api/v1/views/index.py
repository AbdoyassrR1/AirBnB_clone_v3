#!/usr/bin/python3
""" index module"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})
