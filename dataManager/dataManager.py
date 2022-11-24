from enum import Enum
from typing import TypedDict

from bson.objectid import ObjectId

from dataManager.caricaFile import *

"""
Libreria Per Operazioni su db - Implementazione Singleton
Stefano Marrone
Michele Di Giovanni
11-2022
"""


class RequestType(Enum):
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

    def init_client(self, client: pymongo.MongoClient):
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
                'request_type': 'FULL'/'PLAIN'/'SPEECH'/'HANDWRITING'/'EEG'
                'payload': ..
            }
        ]
        request_type: 
            - FULL, si inserisce il paziente con tutte le informazioni relative
            - PLAIN, si inserisce solo un plain file relativo ad un paziente
            - SPEECH, si inserisce solo un file speech relativo ad un paziente
            ....
        payload:
            A seconda della request type il payload può variare.
            Nel caso FULL (unico fin ora implementato) il payload è composto da una lista di pazienti con i loro dati 
            anagrafici e la lista dei file da caricare (gia presenti sul fs) per ogni paziente
        N.B. la variabile data deve essere creata a partire da un json nel seguente modo:
        data = json.loads(json_data)
        in questo modo converto il file json in un dizionario python

    """

    def insert_patient_data(self, data):
        payloadConst = 'payload'
        patientIdentifierConst = 'patientIdentifier'
        patientInfoConst = 'patient'
        requestTypeConst = 'request_type'
        collection = self.db.patient
        pids = []
        for obj in data:
            # controllo se l'id già esiste
            payload = obj[payloadConst]
            # se non c'è il campo patientIdentifier nel record esco
            patient = payload['patient']
            if patientIdentifierConst not in patient:
                return False
            # se il paziente non esiste lo inserisco
            res = collection.find_one({patientIdentifierConst: patient[patientIdentifierConst]})
            if not res:
                collection.insert_one(patient)

            if obj[requestTypeConst] == RequestType.FULL:
                row = payload
                pid = row[patientInfoConst][patientIdentifierConst]
                pids.append(pid)
                insertHandwriting(self.fs, collection, self.db, row)
                insertEEG(self.fs, collection, self.db, row)
                insertSpeech(self.fs, collection, self.db, row)
            elif obj[requestTypeConst] == RequestType.PLAIN:
                # insertPlainFiles(fs,)
                pass
            elif obj[requestTypeConst] == RequestType.SPEECH:
                # insertSpeech(fs, col, db, row)
                pass
            elif obj[requestTypeConst] == RequestType.HANDWRITING:
                pass
            elif obj[requestTypeConst] == RequestType.EEG:
                pass
        return pids


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataManager(DataManagerBase, metaclass=Singleton):
    pass
