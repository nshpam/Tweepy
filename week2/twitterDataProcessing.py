import pandas as pd
import pymongo
import config

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)

#database name
mydb = myclient[config.database_name]
#collection name
mycol = mydb[config.collection_name]

cursor = mycol.find()

for doc in cursor:
    print(doc)
    
# Close the connection to MongoDB when you're done.
myclient.close()