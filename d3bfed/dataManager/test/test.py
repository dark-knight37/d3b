import unittest

import pymongo as pymongo

from d3bfed.dataManager.dataManager import DataManager, RequestType


class MyTestCase(unittest.TestCase):
    def test_write_data(self):
        # connessione con MongoDB
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        DataManager().init_client(client)
        patient_data = [
            {
                'request_type': RequestType.FULL,
                'payload': {
                    'patient': {
                        "patientIdentifier": "P13",
                        "age": "28",
                        "gender": "Male",
                        "disease": True,
                        "handwrittenList": [
                            'hw1'
                        ],
                        "speechList": [

                        ],
                        "eegList": [
                        ],
                    },
                    'data': {'hw1': 'cHJvdmEgMQ=='}
                },

            }
        ]
        pids = DataManager().insert_patient_data(patient_data)
        self.assertEqual(pids, ['P13'])


if __name__ == '__main__':
    unittest.main()
