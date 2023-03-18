# coding=utf8
import tweepy
import config
import calendar
import datetime
import database_action
import numpy as np

db_action = database_action.DatabaseAction()
collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)

cursor = collection.find({
  "keyword": '#รีวิวหนัง',
  "date": datetime.datetime(2022, 12, 31, 0, 0, 0, 0)
})

if cursor.count()==0:
    print('no data found')
else:
    for doc in cursor:
        print(doc)
        break