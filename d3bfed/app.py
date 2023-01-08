import os
from os.path import dirname, join

import pymongo
from flask import Flask, request
from dotenv import load_dotenv
#import sys
#sys.path.insert(1,'dataManager')

from d3bfed.dataManager.dataManager import DataManager

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_ULR = os.environ.get("MONGO_ULR")

# connessione con MongoDB
client = pymongo.MongoClient(MONGO_ULR)
DataManager().init_client(client)


@app.route("/")
def hello_world():
    return "<p>D3B Federate</p>"


@app.route("/insert_patient_data", methods=['POST'])
def insert_patient_data():
    s = 'Ok'
    c = 201
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            print(data, type(data))
            try:
                pids = DataManager().insert_patient_data(data)
                s = f"Success, insert {' '.join(pids)}"
                c = 200
            except Exception as e:
                print(str(e))
                s = 'Erorr'
                c = 500
    return s, c
