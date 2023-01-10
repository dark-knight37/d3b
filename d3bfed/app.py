import os
from os.path import dirname, join

import pymongo
import requests
from dotenv import load_dotenv
from flask import Flask, request, send_file

from d3bfed.dataManager.dataManager import DataManager


def app_setup():
    response = requests.post(f'{D3BAGENT_URL}registry', json={
        "d3bfed_url": "http://127.0.0.1:5001/",
        "d3bfed_name": D3BFED_NAME
    })
    print(response)


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_ULR = os.environ.get("MONGO_ULR")
D3BAGENT_URL = os.environ.get("D3BAGENT_URL")
D3BFED_NAME = os.environ.get("D3BFED_NAME")

app = Flask(__name__)

app_setup()

# connessione con MongoDB
client = pymongo.MongoClient(MONGO_ULR)
DataManager().init_client(client)


# TODO: implementare registrazione servizio a D3BAgent

@app.route("/")
def hello_world():
    return "<p>D3B Federate</p>"


@app.route("/insert_patient_data", methods=['POST'])
def insert_patient_data():
    s = 'Erorr'
    c = 500
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


@app.route('/get_patient_data', methods=["POST"])
def get_patient_data():
    s = 'Error'
    c = 500
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
        print(data, type(data))
        if 'query' not in data or 'type' not in data:
            s = 'Invalid request'
            c = 400
            return s, c
        try:
            zip_filename = DataManager().read_patient_data_by_query(data['query'], data['type'],
                                                                    kind=data['kind'] if 'kind' in data else None,
                                                                    nature=data['nature'] if 'nature' in data else None)
            print(zip_filename)
            if zip_filename:
                return send_file(zip_filename, as_attachment=True)
            s = f"No patient meets the criteria"
            c = 204
        except Exception as e:
            print(str(e))
            s = 'Erorr'
            c = 500
    return s, c
