import os
import flask
from flask import Flask, request
from datetime import datetime
from pymongo import MongoClient
import socket

app = Flask(__name__)

use_db = os.getenv('NO_DB', "False")

if use_db :
    mongo_uri = os.getenv("MONGO_URI","mongodb://mongodb:27017/")
    client = MongoClient(mongo_uri)
    db = client["web_logs"] 
    collection = db["requests"]

@app.route("/")
def home():
    client_ip = request.remote_addr
    current_date = datetime.now()
    
    # on enregistre l'ip du client avec la date dans MongoDB pour chaque requete
    collection.insert_one({"ip": client_ip, "date": current_date})

    # Your flask application should display the last 10 records of the database
    ##Challenge 3 below
 # Récupérer les 10 derniers enregistrements
    last_10_requests = list(collection.find().sort("_id", -1).limit(10))

    server_hostname = socket.gethostname()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    responses = ""
    
    for req in last_10_requests:
        responses += f"<li>{req['ip']} - {req['date']}</li>"

    # Retourner les informations dans la réponse HTML
    return f"""
    <h1>Bienvenue sur ma page web pour 4255</h1>
    <p>Nom : Sophie Ledrich</p>
    <p>Projet : Challenge 3</p>
    <p>Version : V2</p>
    <p>Hostname : {request.host}</p>
    <p>Date actuelle : {datetime.now()}</p>
    <h2>Dernières connexions :</h2>
    <ul>{responses}</ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
