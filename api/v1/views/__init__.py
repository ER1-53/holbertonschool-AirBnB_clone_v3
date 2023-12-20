#!/usr/bin/python3
"""init api"""
from flask import Blueprint, render_template
from api.v1.views.index import *
from api.v1.views.states import *
app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')
