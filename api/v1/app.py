#!/usr/bin/python3
"""file app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
