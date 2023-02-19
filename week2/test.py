# import pymongo
import config
from dateutil import tz
import datetime
# import database_action
# import collections
# import twitterDataProcessing
import tweepy_main


# data_field = ["_id", "id", "text"]
# data_list = [0, 1, 1]

# db_action = database_action.DatabaseAction()

# collection =  db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)
# query_object = db_action.tweetdb_create_object(data_field, data_list)
# cursor = db_action.tweetdb_show_collection(config.collection_name, collection, query_object)
# all_data = []

# word = """🚐 HBO GO

# 🍊 รวมหนัง / ซีรีส์ดังทั่วโลก
# 🍊 โหลดเก็บไว้ดูออฟไลน์ได้

# 🏞️ สอบถาม/สั่งซื้อ Dm or Line @337lhrzg (https://t.co/pAkHMDvQ2g)

# #หารHBOGO #HBOgoหาร #HBOgoราคาถูก #หารhboราคาถูก #รีวิวหนัง #HBOgo #HBO #หารhbogoราคาถูก #หารhbogoถูก #hbogoพร้อมส่ง https://t.co/kesqwREfKR"""

# my_filter = twitterDataProcessing.FilterData()
# word = my_filter.Filters(word)
# print(word)


# raw_list = word.split()
# clean_json = ''
# for word in raw_list:
#     try:
#         my_filter.FilterUrl(word)
#     except:
#         clean_json+=' '+word

# print(clean_json)


# for doc in cursor:
#     raw_list = doc['text'].split()
#     clean_json = ''

#     for word in raw_list:
#         try :
#             my_filter.FilterUrl(word)
#         except:
#             clean_json += ' '+word
#     # print(clean_json)
#     all_data.append(clean_json)

# # print(all_data)
    

# x = dict(collections.Counter(all_data))
# x = dict(sorted(x.items(), key=lambda item: item[1], reverse=True))

# print(x)





# y = """🚐 HBO GO

# 🍊 รวมหนัง / ซีรีส์ดังทั่วโลก
# 🍊 โหลดเก็บไว้ดูออฟไลน์ได้

# 🏞️ สอบถาม/สั่งซื้อ Dm or Line @337lhrzg (https://t.co/pAkHMDvQ2g)

# #หารHBOGO #HBOgoหาร #HBOgoราคาถูก #หารhboราคาถูก #รีวิวหนัง #HBOgo #HBO #หารhbogoราคาถูก #หารhbogoถูก #hbogoพร้อมส่ง https://t.co/kesqwREfKR"""

# if x == y:
#     print('yes')

#timezone of your variable
from_zone = tz.gettz('UTC')
#timezone you want to convert
to_zone = tz.gettz(config.local_timezone)

x = tweepy_main.PullTwitterData().convert_timezone(from_zone, to_zone, datetime.datetime.utcnow())
print(x)