import pymongo
import config

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)
#database name
mydb = myclient[config.database_name]
#collection name
mycol = mydb[config.collection_name]

cursor = mycol.find({"id":"16121091879454124304"})
# cursor = mycol.find({"id":"1612109187949154304"})

have = False

# print(cursor)
print(list(cursor))



print(have)