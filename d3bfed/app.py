import pymongo
from flask import Flask

from ..dataManager import DataManager

app = Flask(__name__)

# connessione con MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
DataManager().init_client(client)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
