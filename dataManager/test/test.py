import unittest

from d3b.dataManager.dataManager import *


class MyTestCase(unittest.TestCase):
    def test_write_data(self):
        # connessione con MongoDB
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        DataManager().init_client(client)
        patient_data = [
            {
                'request_type': RequestType.FULL,
                'payload': {
                    "patientIdentifier": "P13",
                    "age": "28",
                    "gender": "Male",
                    "disease": True,
                    "handwrittenList": [
                    ],
                    "speechList": [

                    ],
                    "eegList": [
                    ]
                },
            }
        ]
        pids = DataManager().insert_patient_data(patient_data)
        self.assertEqual(pids, ['P13'])


if __name__ == '__main__':
    unittest.main()
