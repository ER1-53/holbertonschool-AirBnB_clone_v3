#!/usr/bin/python3
from flask import Blueprint, render_template
app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')
from api.v1.views.index import *

@app_views.route('/')
def index():
    return render_template('index.html')
