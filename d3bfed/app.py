from flask import Flask, request

from d3b.dataManager.dataManager import *

app = Flask(__name__)

# connessione con MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
DataManager().init_client(client)


@app.route("/")
def hello_world():
    return "<p>D3B Federate</p>"


@app.route("/insert_patient_data", methods=['POST'])
def insert_patient_data():
    if request.method == 'POST':
        print(request.form)
