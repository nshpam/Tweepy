import config
# from dateutil import tz
import datetime
import database_action
# import collections
import twitterDataProcessing

# db_action = database_action.DatabaseAction()

# start_collection =  db_action.tweetdb_object(config.mongo_client, config.database_name, config.old_collection)
# des_collection =  db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

# #field for start database
# data_field_1 = ["_id", "id", "username", "date", "time", "text", "favorite_count", "retweet_count"]
# data_list_1 = [0, 1, 1, 1, 1, 1, 1, 1]

# #field for des database
# data_field_2 = ["_id", "id", "keyword", "username", "date", "location", "text", "favorite_count", "retweet_count"]
# data_list_2 = [0, 1, 1, 1, 1, 1, 1, 1, 1]

# query_object_1 = db_action.tweetdb_create_object(data_field_1, data_list_1)
# query_object_2 = db_action.tweetdb_create_object(data_field_2, data_list_2)

# collection_1 = db_action.tweetdb_object(config.mongo_client, config.database_name, config.old_collection)
# collection_2 = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

# cursor_1 = db_action.tweetdb_show_collection(config.collection_name, collection_1, query_object_1)
# cursor_2 = db_action.tweetdb_show_collection(config.collection_name, collection_2, query_object_2)

# my_filter = twitterDataProcessing.FilterData()
# check_dict = {}
# data_dict = {}

# db_action.not_print_raw()

# #get all data from old database
# for doc in cursor_1:
#     raw_list = doc['text'].split()
#     clean_json = ''

#     #filter the url from word
#     for word in raw_list:
#         if not my_filter.FilterUrl(word):
#             clean_json += word

#     if clean_json not in list(check_dict.values()):
#         #reversing the str format into datetime
#         dt = datetime.datetime.strptime(doc['date']+' '+doc['time']+':00', '%d-%m-%Y %H:%M:%S')

#         #convert it to iso format and convert it into datetime data type
#         dt = datetime.datetime.fromisoformat(dt.isoformat())

#         #create the data object
#         temp_data_list = [int(doc['id']),'#รีวิวหนัง', doc['username'], dt, None, doc['text'], doc['favorite_count'], doc['retweet_count']]
#         data_object = db_action.tweetdb_create_object(data_field_2[1:], temp_data_list)

#         #dictionary for checking
#         check_dict[doc['id']] = clean_json
#         data_dict[doc['id']] = data_object

# # print('filtered :',len(list(check_dict.values())))

# data_list = list(data_dict.values())

# # #insert the data to cleaned_data
# for i in range(len(data_list)):
#     db_action.tweetdb_insert(config.collection_name, collection_2, data_list[i])

# print('finish')

# print(all_data)

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
# from_zone = tz.gettz('UTC')
# #timezone you want to convert
# to_zone = tz.gettz(config.local_timezone)

# dt = datetime.datetime.fromisoformat("2023-02-19T14:57:25.000+00:00")

# print(dt)

# # x = tweepy_main.PullTwitterData().convert_timezone(from_zone, to_zone, datetime.datetime.utcnow())
# # x = dt.date()
# print(x)

# from opencage.geocoder import OpenCageGeocode
# geocoder = OpenCageGeocode(config.opencage_key)
# location_info_list = geocoder.geocode("วัดดีบอน ราชบุรี, ประเทศไทย")
# for x in location_info_list:
#     print(x.keys())
#     print(x)
# print(location_info_list)

import tweepy
import config

# Authenticate to Twitter API
auth = tweepy.OAuth1UserHandler(config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret)
api = tweepy.API(auth)

tweets = tweepy.Cursor(
         api.search_tweets ,
         q='#อาหาร' + ' -filter:retweets', 
         tweet_mode=config.search_mode,
         result_type=config.search_type
         ).items(config.num_tweet)
# Check if the user exists
try:
    for tweet in tweets:
        
        # Get the latest tweet from the user
   
    # Check if the tweet has a place
        if tweet.place:
            # Print the location of the tweet
            print(tweet.place)
        else:
            print("No location information available.")
except tweepy.TweepError as error:
    if error.api_code == 34:
        print("User does not exist.")
    else:
        print(error)
# print(location_info_list[0].keys())
    #   if location_info_list:
    #      location_info = location_info_list[0]
    #      if location_info.get('status', {}).get('code') == 200:
    #         location_name = location_info.get('formatted')
    #         country = location_info.get('components', {}).get('country')

    #   else:
    #      tweet_location = None