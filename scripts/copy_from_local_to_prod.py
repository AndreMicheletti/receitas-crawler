from pymongo import MongoClient
from database import MONGO_CONN_STRING_MASTER, LOCAL_CONN_STRING

# CONNECT TO PROD
master_db = MongoClient(MONGO_CONN_STRING_MASTER)['recipes']
# CONNECT TO LOCAL
local_db = MongoClient(LOCAL_CONN_STRING)['recipes']

input("START COPYING? [enter]")

count = 0

for doc in local_db.get_collection('recipe').find():
    master_db.get_collection('recipe').insert_one(doc)
    count += 1

print(f'COPIED {count} DOCS!')
print('END!')
