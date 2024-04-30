#!/usr/bin/python3
"""create app_views Blueprint"""

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *


app_views = Blueprint("base", __name__, url_prefix="/api/v1")
