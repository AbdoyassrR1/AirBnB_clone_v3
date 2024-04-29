#!/usr/bin/python3
""" flask app """
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def teardown(exception):
    """ call storage.close"""
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True, debug=True)
