import pandas as pd
import pymongo
import config
import requests
#import Api LexTo+
Apikey = 'Ex0WSb2UFAyfDXRU8vLwkeR04N6e58Tq'
url = 'https://api.aiforthai.in.th/lextoplus'

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)

#database name
mydb = myclient[config.database_name]
#collection name
mycol = mydb[config.collection_name]
#select only text
cursor = mycol.find({},{ "_id": 0, "text": 1})

for doc in cursor:
    print(doc)
    
# Close the connection to MongoDB when you're done.
myclient.close()
