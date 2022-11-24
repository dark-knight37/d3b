#!/usr/bin/python3

import base64
import json

import gridfs
import pymongo


def insertPlainFiles(filesystem, column, database, patientID, filelist, tag, filekind, payload):
    for fname in filelist:
        # fhandle = open(fname, 'rb')
        # data = fhandle.read()

        # il dato è caricato direttamente nel payload

        if fname not in payload:
            pass

        data = payload[fname]
        base64_bytes = data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        item = filesystem.put(message, patient_id=patientID, filename=fname, kind=filekind, encoding='utf-8')
        column.update_many({"patientIdentifier": patientID}, {"$set": {tag: filelist}})
        #res = column.find({"patientIdentifier": patientID})
        #for result in res:
        #    P_id = result["_id"]
        #    database.fs.files.update_many({"patient_id": patientID}, {"$set": {"patient_id": P_id}})


def insertSpeech(filesystem, column, database, row):
    patientID = row['patient']['patientIdentifier']
    for entry in row['patient']['speechList']:
        kkind = entry["kind"]
        nnature = entry["nature"]
        fname = entry["fname"]
        # fhandle = open(fname, 'rb')
        # data = fhandle.read()
        if entry not in row['data']:
            pass
        data = row['data'][fname]
        item = filesystem.put(data, patient_id=patientID, filename=fname, nature=nnature, kind=kkind)
        column.update_many({"patientIdentifier": patientID}, {"$set": {"speechList": row['speechList']}})
        res = column.find({"patientIdentifier": patientID})
        for result in res:
            P_id = result["_id"]
            database.fs.files.update_many({"patient_id": patientID}, {"$set": {"patient_id": P_id}})


def insertHandwriting(filesystem, column, database, row):
    pid = row['patient']['patientIdentifier']
    hwlist = row['patient']['handwrittenList']
    insertPlainFiles(filesystem, column, database, pid, hwlist, "handwrittenList", "handwriting", row['data'])


def insertEEG(filesystem, column, database, row):
    pid = row['patient']['patientIdentifier']
    eeglist = row['patient']['eegList']
    insertPlainFiles(filesystem, column, database, pid, eeglist, "eegList", "eeg", row['data'])


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.androids
    db.patient.drop()
    db.fs.files.drop()
    db.fs.chunks.drop()
    col = db.patient
    file_json = open('../data.json', 'r')
    data_from_json = json.loads(file_json.read())
    fs = gridfs.GridFS(db)
    for row in data_from_json:
        col.insert_one(row)
        # pid = row['patientIdentifier']
        insertHandwriting(fs, col, db, row)
        # insertEEG(fs, col, db, row)
        # insertSpeech(fs, col, db, row)
