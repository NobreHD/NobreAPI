from flask import jsonify
import json, time

file = "data/petting.json"
saved = {}
last_request = 0

def petting():
    global last_request, saved
    if time.time() - last_request > 60:
        last_request = time.time()
        with open(file, "r") as f:
            saved = json.loads(f.read())
    return jsonify(saved)

def setup(app):
    global saved
    app.add_url_rule('/petting', 'petting', petting, methods=['GET'])
    with open(file, "r") as f:
        saved = json.loads(f.read())
    print("Petting Routes Loaded")


