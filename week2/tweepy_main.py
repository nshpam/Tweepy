#import file
import config 

#import library
import tweepy     #use for twitter scrapping
import pymongo    #use for connecting to mongodb
from dateutil import tz #use for timezone converting
import datetime   #use for timezone converting

#you can edit mongodb server, database name, collection name in file name "config.py"

#connect to mongodb server with pymongo
myclient = pymongo.MongoClient(config.mongo_client)
#choose database name
mydb = myclient[config.database_name]
#choose collection name
mycol = mydb[config.collection_name]

#scrap twitter data from Twitter API
class PullTwitterData(object):

   #initialize variable
   def __init__(self, tweets_list=[], tweet_object={}):
      self.tweets_list = tweets_list
      self.tweet_object = tweet_object

   #convert timezone from UTC to GMT
   #you can edit the pair of timezone you want in file name "config.py"
   def convert_timezone(self, from_zone, to_zone, convert_date):

      #in case that convert_date not datatime
      if type(convert_date) != type(datetime.datetime.utcnow()):
         time_err_1 = 'Timezone type is not datetime'
         return time_err_1
      
      #in case that from_zone not timezone
      if type(from_zone) != type(tz.gettz('UTC')):
         time_err_2 = 'Timezone type is not timezone'
         return time_err_2
      
      #in case that to_zone not timezone
      if type(to_zone) != type(tz.gettz('Thailand/Bangkok')):
         time_err_3 = 'Timezone type is not timezone'
         return time_err_3

      #convert timezone and change format into day-month-year | hour-minute
      convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%d-%m-%Y | %H:%M')
      return convert_date

   # update database base on tweet id
   def update_database(self, collection_variable, tweet_id, update_fav, update_retweet):
      
      #value for update
      new_values = {"$set":{
      "favorite_count": update_fav,
      "retweet_count": update_retweet}}

      #update database base on id
      cmd = collection_variable.update_one({"id":tweet_id}, new_values)

      return cmd

   #create tweet object for database insertion
   def create_tweet_object(self,id,username,date,time,text,fav_count,retw_count):
      self.tweet_object = {
         'id' : id,
         'username' : username, 
         'date' : date,
         'time' : time,
         'text' : text,
         'favorite_count' : fav_count,
         'retweet_count' : retw_count }
      
      return self.tweet_object


   #insert object into database
   def insert_database(self, data, collection_variable):

      #command for insert object to mongodb
      #insert to the specified collection
      cmd = collection_variable.insert_one(data)
         
      return cmd

   #scarp twitter
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

      #count tweet
      count_tweets = 0

      #timezone of your variable
      from_zone = tz.gettz('UTC')
      #timezone you want to convert
      to_zone = tz.gettz(config.local_timezone)

      #iterate the Tweet in tweets_list
      for tweet in self.tweets_list:

         #tweet id
         tweet_id = str(tweet.id)

         #tweet author
         tweet_username = tweet.user.screen_name

         #tweet date
         tweet_date = tweet.created_at

         #favorite count
         fav_count = tweet.favorite_count

         #retweet count
         retweet_count = tweet.retweet_count

         #get tweet text
         try:
            tweet_text = tweet.retweeted_status.full_text
         except AttributeError:
            tweet_text = tweet.full_text

         #convert time zone from UTC to GMT+7
         #format the date
         tweet_date = self.convert_timezone(from_zone, to_zone, tweet_date)
         tweet_date = tweet_date.split(' | ')
         tweet_time = tweet_date[1]
         tweet_date = tweet_date[0]

         #create tweet object
         self.create_tweet_object(tweet_id,tweet_username,tweet_date,tweet_time,tweet_text,fav_count,retweet_count)

         #query id in database
         cursor = mycol.find({"id":tweet_id})

         #if found then update data
         if list(cursor) != []:
            print('Update duplicate ID :', tweet_id)

            #update retweets, favorites
            self.update_database(mycol, tweet_id, fav_count, retweet_count)

            #count tweets that are updated
            count_tweets+=1

            #close database
            myclient.close()
            
            continue
         else:
            print('Insert ID :', tweet_id)

            #insert to database
            self.insert_database(self.tweet_object, mycol)

            #close database
            myclient.close()

         #count Tweet that is inserted
         count_tweets+=1

      #finish text for unittest
      finish_text = 'TOTAL TWITTER : %d'%count_tweets

      print(finish_text)
   
      return finish_text
