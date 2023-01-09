#!/usr/bin/python3

import base64
import json

import gridfs
import pymongo


def get_file_infos(entry):
    data = entry['data']
    kkind = entry["kind"]
    nnature = entry["nature"] if "nature" in entry["nature"] else None
    fname = entry["fname"]
    fformat = fname.split('.')
    fformat = fformat[1] if len(fformat) > 1 else None
    return {
        'filename': fname,
        'type': 'speechlist',
        'nature': nnature,
        'data': data,
        'format': fformat,
        'kind': kkind
    }


def insertPlainFiles(filesystem, column, patientID, filelist, tag, filetype, payload):
    for fname in filelist:
        # il dato è caricato direttamente nel payload in formato base64

        if fname not in payload:
            pass

        data = payload[fname]
        fformat = fname.split('.')
        fformat = fformat[1] if len(fformat) > 1 else None

        file_infos = {
            'filename': fname,
            'type': filetype,
            'data': data,
            'format': fformat,
            'kind': None,
            'nature': None
        }

        message = base64.b64decode(file_infos['data'])

        item = filesystem.put(message,
                              patient_id=patientID,
                              filename=file_infos['filename'],
                              type=file_infos['type'],
                              kind=file_infos['kind'],
                              format=file_infos['format'],
                              nature=file_infos['nature'],
                              encoding='utf-8')
        column.update_many({"patientIdentifier": patientID}, {"$set": {tag: filelist}})


def insertSpeech(filesystem, column, row, type):
    patientID = row['patient']['patientIdentifier']
    for entry in row['patient']['speechList']:

        file_infos = get_file_infos(entry=entry)

        if file_infos['filename'] not in row['data']:
            pass
        data = row['data'][file_infos['filename']]
        item = filesystem.put(data,
                              patient_id=patientID,
                              filename=file_infos['filename'],
                              type=type,
                              kind=file_infos['kind'],
                              format=file_infos['format'],
                              nature=file_infos['nature'],
                              encoding=None)
        column.update_many({"patientIdentifier": patientID}, {"$set": {"speechList": row['speechList']}})


def insertHandwriting(filesystem, column, row, type):
    pid = row['patient']['patientIdentifier']
    hwlist = row['patient']['handwrittenList']
    insertPlainFiles(filesystem, column, pid, hwlist, "handwrittenList", type, row['data'])


def insertEEG(filesystem, column, row, type):
    pid = row['patient']['patientIdentifier']
    eeglist = row['patient']['eegList']
    insertPlainFiles(filesystem, column, pid, eeglist, "eegList", type, row['data'])


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.androids
    db.patient.drop()
    db.fs.files.drop()
    db.fs.chunks.drop()
    col = db.patient
    file_json = open('../../data.json', 'r')
    data_from_json = json.loads(file_json.read())
    fs = gridfs.GridFS(db)
    for row in data_from_json:
        col.insert_one(row)
        # pid = row['patientIdentifier']
        insertHandwriting(fs, col, db, row)
        # insertEEG(fs, col, db, row)
        # insertSpeech(fs, col, db, row)
