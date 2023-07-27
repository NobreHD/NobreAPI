from flask import jsonify
import json, time

with open("data/petting.json", "r") as f:
    saved = json.loads(f.read())
last_request = 0

def petting():
    return jsonify(saved)

def setup(app):
    global saved
    app.add_url_rule('/petting', 'petting', petting, methods=['GET'])
    print("Petting Routes Loaded")


