import unittest

import pymongo as pymongo
from bson import ObjectId

from d3bfed.dataManager.dataManager import DataManager, D3BDataType


class MyTestCase(unittest.TestCase):
    def test_write_data(self):
        # connessione con MongoDB
        client = pymongo.MongoClient('mongodb://root:example@127.0.0.1:27018/')
        DataManager().init_client(client)
        pid = "P1"
        patient_data = [
            {
                'payload': {
                    'patient': {
                        "patientIdentifier": pid,
                        "age": "28",
                        "gender": "Male",
                        "disease": True,
                        "handwrittenList": [
                            'hw1.txt'
                        ],
                        "speechList": [

                        ],
                        "eegList": [
                        ],
                    },
                    'data': {'hw1.txt': 'cHJvdmEgMQ=='}
                },

            }
        ]
        pids = DataManager().insert_patient_data(patient_data)
        self.assertEqual(pids, [pid])

    def test_read_patient_data_by_id(self):
        client = pymongo.MongoClient('mongodb://root:example@127.0.0.1:27018/')
        DataManager().init_client(client)
        patient_id = 'P13'
        patient = DataManager().read_patient_data_by_id(patient_id)
        print(patient)
        self.assertEqual(
            patient,
            {
                "_id": ObjectId("63bace176c428cdfa7621b1e"),
                "age": "28",
                "disease": True,
                "eegList": [],
                "gender": "Male",
                "handwrittenList": ["hw1"],
                "patientIdentifier": "P13",
                "speechList": []
            }
        )

    def test_read_patient_data_by_query(self):
        client = pymongo.MongoClient('mongodb://root:example@127.0.0.1:27018/')
        DataManager().init_client(client)
        query = {"disease": False, "gender": "Male"}
        type = D3BDataType.HANDWRITING.name
        # print(type)
        DataManager().read_patient_data_by_query(query, type, kind=None, nature=None)


if __name__ == '__main__':
    unittest.main()
