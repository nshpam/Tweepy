import tweepy
import pymongo
from dateutil import tz
import config
import datetime

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)
#database name
mydb = myclient[config.database_name]
#collection name
mycol = mydb[config.collection_name]

cursor = mycol.find({},{ "_id": 0, "id": 1})

class PullTwitterData():

   def __init__(self, insertion=False, tweet_list=[], set_id=set()):
      self.insertion = insertion
      self.tweet_list = tweet_list
      self.set_id = set_id

      self.initialize_id()

   def initialize_id(self):
      # print(cursor)
      for doc in cursor:
         # print(doc)
         
         self.set_id.add(doc['id'])
      
      # print(self.set_id)
      

   #convert timezone from UTC to GMT
   #fixed time zone
   def convert_timezone(self, from_zone, to_zone, convert_date):
      if type(convert_date) != type(datetime.datetime.utcnow()):
         x = 'Timezone type is not datetime'
         return x
      if type(from_zone) != type(tz.gettz('UTC')):
         y = 'Timezone type is not timezone'
         return y
      if type(to_zone) != type(tz.gettz('Thailand/Bangkok')):
         z = 'Timezone type is not timezone'
         return z
      #convert timezone and change format into day-month-year | hour-minute
      convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%d-%m-%Y | %H:%M')
      return convert_date

   #update database
   def update_database(self, collection_variable, tweet_id, update_fav, update_retweet):
      for doc in cursor:
         if tweet_id == doc['id']:
            new_values = {"$set":{
               "favorite_count": update_fav,
               "retweet_count": update_retweet}}
            cmd = collection_variable.update_one({"id":tweet_id}, new_values)
            return cmd
      

   #insert object into database
   def insert_database(self, data, collection_variable):

      #command for insert object to mongodb
      #insert to the specified collection
      cmd = collection_variable.insert_one(data)
         
      return cmd

   def search_twitter(self, api):

      #use Cursor to serach
      #tweepy.Cursor(search API, word + filter, search mode, search type).items(search limit)
      tweets = tweepy.Cursor(
         api.search_tweets ,
         q=config.search_word + ' -filter:retweets', 
         tweet_mode=config.search_mode,
         result_type=config.search_type
         ).items(config.num_tweet)

      #create a list of Tweets
      self.tweets_list = [tweet for tweet in tweets]

      count_tweets = 0
      #timezone of your variable
      from_zone = tz.gettz('UTC')
      #timezone you want to convert
      to_zone = tz.gettz(config.local_timezone)

      # print(len(self.tweets_list))

      #iterate the Tweet in tweets_list
      for tweet in self.tweets_list:

         #tweet id
         tweet_id = tweet.id

         #tweet author
         tweet_username = tweet.user.screen_name

         #tweet date
         tweet_date = tweet.created_at

         #favorite count
         fav_count = tweet.favorite_count

         #retweet count
         retweet_count = tweet.retweet_count


         if str(tweet_id) in self.set_id:
            print('Update duplicate ID', tweet_id)
            self.update_database(mycol, tweet_id, fav_count, retweet_count)
            continue
         else:
            print('insertion begin')

            #convert time zone from UTC to GMT+7
            tweet_date = self.convert_timezone(from_zone, to_zone, tweet_date)
            tweet_date = tweet_date.split(' | ')
            tweet_time = tweet_date[1]
            tweet_date = tweet_date[0]

            #get tweet text
            try:
               tweet_text = tweet.retweeted_status.full_text
            except AttributeError:
               tweet_text = tweet.full_text
            
            # create tweet object
            tweet_object = {
               'id' : str(tweet_id),
               'username' : tweet_username, 
               'date' : tweet_date,
               'time' : tweet_time,
               'text' : tweet_text,
               'favorite_count' : fav_count,
               'retweet_count' : retweet_count }

            #insert to database
            self.insert_database(tweet_object, mycol)
            myclient.close()

         #count Tweet that is inserted
         count_tweets+=1

      finish_text = 'TOTAL TWITTER : %d'%count_tweets

      print(finish_text)

      return finish_text
