#!/usr/bin/python3

import pymongo
import gridfs

client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')

db=client.androids
fs=gridfs.GridFS(db)
query = db.patient.find({"disease":"False", "gender":"Male"})
for result in list(query):
  p_id = result["_id"]
  q = db.fs.files.find({"patient_id":p_id, "kind":"diary", "nature":"audio"})
  for x in q:
    name = x["filename"]
    outputdata = fs.get_last_version(name).read()
    output = open('out_' + name, "wb")
    output.write(outputdata)
    output.close()
print('Download completato!')