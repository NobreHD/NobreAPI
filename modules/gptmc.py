from flask import jsonify
import json

data_file = "data/gptmc.json"

def gptmc():
    data = {
        "name": "GPT-MC",
        "description": "GPT-3 for Minecraft commands"
    }
    with open(data_file, "r") as f:
        data["training_data"] = json.loads(f.read())
    data["count"] = len(data["training_data"])
    return jsonify(data)

def setup(app):
    app.add_url_rule('/gptmc', 'gptmc', gptmc, methods=['GET'])
    print("GPT-MC Routes Loaded")
        