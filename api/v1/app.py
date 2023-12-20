#!/usr/bin/python3
"""file app"""
from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def page_not_found(exception):
    """404 error"""
    error = {"error":"Not found"}
    return jsonify(error), 404


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, debug=True)
