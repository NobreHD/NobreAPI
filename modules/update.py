from flask import request, jsonify
from dotenv import load_dotenv
from threading import Thread
import os, hmac, hashlib, time

load_dotenv()

SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')

def update_thread():
    time.sleep(2)
    os.system("git pull")

def update():
    signature = request.headers.get('x-hub-signature-256')
    if signature is None or signature == "":
        return "No signature", 403
    hash = hmac.new(SECRET.encode('utf-8'), msg=request.data, digestmod=hashlib.sha256).hexdigest()
    expected = f"sha256={hash}"
    if not hmac.compare_digest(signature, expected):
        return "Invalid signature", 403
    
    event = request.headers.get('x-github-event')
    if event is None or event == "":
        return "No event", 403
    if event == "ping":
        return jsonify({"msg": "pong"})
    if event != "push":
        return "Invalid event", 403
    
    Thread(target=update_thread).start()
    return "OK", 200
    
def setup(app):
    app.add_url_rule('/update', 'update', update, methods=['POST'])
    print("Update Routes Loaded")