from enum import Enum
from typing import TypedDict

from bson.objectid import ObjectId

from caricaFile import *

"""
Libreria Per Operazioni su db - Implementazione Singleton
Stefano Marrone
Michele Di Giovanni
11-2022
"""


class FileType(Enum):
    FULL = 0
    PLAIN = 1
    SPEECH = 2
    HANDWRITING = 3
    EEG = 4


class D3BSpeechData(TypedDict):
    kind: str
    nature: str
    fname: str


class D3BData(TypedDict):
    _id: ObjectId
    age: int
    disease: bool
    eegList: list[str]
    gender: str
    handwrittenList: list[str]
    patientIdentifier: str
    speechList: list[D3BSpeechData]


class DataManagerBase:
    def __init__(self):
        self.client: pymongo.MongoClient = None
        self.db: pymongo.collection.Collection[D3BData] = None
        self.fs: gridfs.GridFS = None

    def init_client(self, client):
        self.client = client
        self.db = client.androids
        self.fs = gridfs.GridFS(self.db)
        # self.db.patient.drop({})
        # self.db.fs.files.drop({})
        # self.db.fs.chunks.drop({})

    """
        write_file è un wrapper delle funzioni  per inserire i file definite in caricaFile.py
        il metodo si aspetta un dato così strutturato:
        data = [
            {
                'file_type': 'FULL'/'PLAIN'/'SPEECH'/'HANDWRITING'/'EEG'
                'payload': ..
            }
        ]
        N.B. la variabile data deve essere creata a partire da un json nel seguente modo:
        data = json.loads(json_data)
        in questo modo converto il file json in un dizionario python

    """

    def write_file(self, data):
        collection = self.db.patient
        for obj in data:
            collection.insert_one(obj['payload'])
            match obj['file_type']:
                case FileType.FULL:
                    pid = row['patientIdentifier']
                    insertHandwriting(fs, col, db, row)
                    insertEEG(fs, col, db, row)
                    insertSpeech(fs, col, db, row)
                case FileType.PLAIN:
                    # insertPlainFiles(fs,)
                    pass
                case FileType.SPEECH:
                    #insertSpeech(fs, col, db, row)
                    pass
                case FileType.HANDWRITING:
                    pass
                case FileType.EEG:
                    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataManager(DataManagerBase, metaclass=Singleton):
    pass
