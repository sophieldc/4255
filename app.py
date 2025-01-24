import os
from flask import Flask, request, jsonify
from datetime import datetime   
import socket

app = Flask(__name__)

# Vérifiez si la version actuelle est "nodb"
NO_DB = os.getenv("NO_DB", "false").lower() == "true"

if not NO_DB:
    from pymongo import MongoClient
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client['flask_db']
    collection = db['requests']

# Informations sur le projet
PROJECT_NAME = "My Project"
VERSION = "V3"
NAME = "Sophie Ledrich"

@app.route("/")
def flaskTest():
    client_ip = request.remote_addr
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not NO_DB:
        collection.insert_one({"ip": client_ip, "date": current_date})
        last_requests = collection.find().sort("_id", -1).limit(10)
        responses = "<ul>"
        for req in last_requests:
            responses += f"<li>{req['ip']} - {req['date']}</li>"
        responses += "</ul>"
        return f"<h1>Hello from Flask (DB)</h1><p>Your IP: {client_ip}</p><p>Last 10 requests:</p>{responses}"

    else:
        return f"<h1>Hello from Flask (NO DB)</h1><p>Your IP: {client_ip}</p><p>Current Date: {current_date}</p>"

@app.route("/healthz")
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)       