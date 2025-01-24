import os
from flask import Flask, request
from pymongo import MongoClient
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
        return f"""
        <h1>Bienvenue sur ma page Flask DB pour 4255</h1>
        <p>Nom : Sophie Ledrich</p>
        <p>Projet : Challenge 6</p>
        <p>Version : V3</p>
        <p>Hostname : {client_ip}</p>
        <p>Date actuelle : {current_date}</p>
        <h2>Dernières connexions :</h2>
        <ul>{responses}</ul> """

    else:
        return f"<h1>Hello from Flask (NO DB)</h1><p>Your IP: {client_ip}</p><p>Current Date: {current_date}</p>
        <h1>Bienvenue sur ma page Flask NO DB pour 4255</h1>
        <p>Nom : Sophie Ledrich</p>
        <p>Projet : Challenge 6</p>
        <p>Version : V3</p>
        <p>Hostname : {client_ip}</p>
        <p>Date actuelle : {current_date}</p>
        <h2>Dernières connexions :</h2>
        <ul>{responses}</ul> """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)       
