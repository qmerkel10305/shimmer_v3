from flask import Flask, request
import requests
import json
import pprint

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)

# Response for GET business request
@app.route("/image", methods=['GET'])
def getImage():
    return ""

# Register your name
@app.route("/target", methods=['POST'])
def target():
    print json.dumps(json.loads(request.data), indent=4, sort_keys=True)
    return "thx"

# if '> python this.py' run Flask
if __name__ == "__main__":
    app.run()
