from flask import jsonify
import json, time

with open("data/bsr.json", "r") as f:
    saved = json.loads(f.read())
last_request = 0

def url_patch():
    return jsonify(saved)

def setup(app):
    global saved
    app.add_url_rule('/bsr', 'url_patch', url_patch, methods=['GET'])
    print("BSR Routes Loaded")