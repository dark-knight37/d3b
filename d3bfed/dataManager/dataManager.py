import json
import zipfile
from enum import Enum
from typing import TypedDict

import gridfs
import pymongo
from bson.objectid import ObjectId

from .caricaFile import insertHandwriting, insertEEG, insertSpeech

"""
Libreria Per Operazioni su db - Implementazione Singleton
Stefano Marrone
Michele Di Giovanni
11-2022
"""


class D3BDataType(Enum):
    PLAIN = 0
    HANDWRITING = 1
    SPEECH = 2
    EEG = 3


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
        self.payload_const = 'payload'
        self.patient_identifier_const = 'patientIdentifier'
        self.patient_info_const = 'patient'

    def init_client(self, client: pymongo.MongoClient):
        self.client = client
        self.db = client.androids
        self.fs = gridfs.GridFS(self.db)
        # self.db.patient.drop({})
        # self.db.fs.files.drop({})
        # self.db.fs.chunks.drop({})

    """
        insert_patient_data è un wrapper delle funzioni  per inserire i file definite in caricaFile.py
        il metodo si aspetta un dato così strutturato:
        data = [
            {
                'payload': {
                    'patient': {
                        "patientIdentifier":..,
                        "age": ..,
                        "gender":..,
                        "disease": ..,
                        "handwrittenList": [
                            "hw1",
                            ...
                        ],
                        "speechList": [
                            ..
                        ],
                        "eegList": [
                            ..
                        ],
                    },
                    'data': {'hw1': 'cHJvdmEgMQ=='}            }
        ]
        payload:
            Il payload è composto da una lista di pazienti con i loro dati anagrafici e la lista dei file da caricare 
            (codificati in base 8) per ogni paziente
    """

    def insert_patient_data(self, data):
        collection = self.db.patient
        pids = []
        for obj in data:
            # controllo se l'id già esiste
            payload = obj[self.payload_const]
            # se non c'è il campo patientIdentifier nel record esco
            patient = payload['patient']
            if self.patient_identifier_const not in patient:
                return False
            # se il paziente non esiste lo inserisco
            res = collection.find_one({self.patient_identifier_const: patient[self.patient_identifier_const]})
            if not res:
                collection.insert_one(patient)
            # if obj[request_type_const] == RequestType.FULL.name:
            row = payload
            pid = row[self.patient_info_const][self.patient_identifier_const]
            pids.append(pid)
            insertHandwriting(self.fs, collection, row, D3BDataType.HANDWRITING.name)
            insertEEG(self.fs, collection, row, D3BDataType.EEG.name)
            insertSpeech(self.fs, collection, row, D3BDataType.SPEECH.name)

            """
            elif obj[request_type_const] == RequestType.PLAIN.name:
                # insertPlainFiles(fs,)
                pass
            elif obj[request_type_const] == RequestType.SPEECH.name:
                # insertSpeech(fs, col, db, row)
                pass
            elif obj[request_type_const] == RequestType.HANDWRITING.name:
                pass
            elif obj[request_type_const] == RequestType.EEG:
                pass
                """
        return pids

    def read_patient_data_by_id(self, patientId):
        query = self.db.patient.find({
            self.patient_identifier_const: patientId
        })
        if query:
            return query[0]
        return None

    """
       read_patient_data_by_query viene utilizzato per infiare i file relativi ai pazienti (handwriting, speech, eeg)
       se i criteri inseriti in query sono rispettati.
       Ad es.
       query = {
            "disease": True, 
            "gender": "Male"
       }
       type = "HANDWRITING"
       Se viene trovato almeno un paziente che rispetta i criteri della query
       viene restituito un file out.zip composto da
       - info.json, contenente gli id dei pazienti e i nomi dei files,
       - lista dei file di tipo type
    """

    def read_patient_data_by_query(self, query, type: D3BDataType, kind=None, nature=None):
        res = self.db.patient.find(query)
        local_filenames = []
        patient_filename_map = {
            'query': query
        }
        for val in res:
            p_id = val[self.patient_identifier_const]
            q = self.db.fs.files.find({
                'patient_id': p_id,
                'type': type,
                'kind': kind,
                'nature': nature
            })
            for x in q:
                if p_id not in patient_filename_map:
                    patient_filename_map[p_id] = {}
                    patient_filename_map[p_id]['filename'] = []
                name = x['filename']
                patient_filename_map[p_id]['filename'].append(name)

                outputdata = self.fs.get_last_version(name).read()
                print(outputdata)
                output = open(name, "wb")
                output.write(outputdata)
                output.close()
                local_filenames.append(name)
        if local_filenames:
            with open('info.json', 'w') as infofile:
                json.dump(patient_filename_map, infofile)
            local_filenames.append('info.json')
            with zipfile.ZipFile('out.zip', 'w') as zipMe:
                for file in local_filenames:
                    zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
            return 'out.zip'
        return None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataManager(DataManagerBase, metaclass=Singleton):
    pass
