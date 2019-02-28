import argparse
import json

from flask import Flask, request, send_file, redirect, url_for
from flask_cors import CORS

from server.models.GlobalModel import init_model
from server.controllers.ImageController import image_api
from server.controllers.TargetController import target_api

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Add api controllers
app.register_blueprint(image_api, url_prefix='/image')
app.register_blueprint(target_api, url_prefix='/target')

@app.route('/')
def index():
    """
    Serves the index page
    """
    return app.send_static_file('index.html')

@app.route('/targets')
def targets():
    """
    Serves the target view page.
    This actually serves the index page, but Angular renders the page this way.
    """
    return app.send_static_file('index.html')

@app.route('/images')
def images():
    """
    Serves the image view page.
    This actually serves the index page, but Angular renders the page this way.
    """
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def root(path):
    """
    Serves static files for the frontend.
    """
    return app.send_static_file(path)

@app.route('/next')
def next_img():
    """
    Redirect to images/next
    """
    return redirect(url_for('image_api.getNext'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog="You must specify either flight or directory.")
    parser.add_argument("-f", "--flight", type=int, help="Flight number")
    args = parser.parse_args()

    init_model(args.flight)

    app.run(host='0.0.0.0')
