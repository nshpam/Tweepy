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

#convert timezone from UTC to GMT
#fixed time zone
def convert_timezone(from_zone, to_zone, convert_date):
   if type(convert_date) != type(datetime.datetime.utcnow()):
      x = 'Timezone type is not datetime'
      return x
   #convert timezone and change format into day-month-year | hour-minute
   convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%d-%m-%Y | %H:%M')
   return convert_date

#insert object into database
def insert_database(data, collection_variable):
   #command for insert object to mongodb
   #insert to the specified collection
   cmd = collection_variable.insert_one(data)
   return cmd

#connect to twitter API
def connect_twitter():
   #input the tokens
   auth = tweepy.OAuth1UserHandler(
      config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
   )
   api = tweepy.API(auth)
   return api

def search_twiter(api):

   #use Cursor to serach
   #tweepy.Cursor(search API, word + filter, search mode, search type).items(search limit)
   tweets = tweepy.Cursor(
      api.search_tweets ,
      q=config.search_word + ' -filter:retweets', 
      tweet_mode=config.search_mode,
      result_type=config.search_type
      ).items(config.num_tweet)

   #create a list of Tweets
   tweets_list = [tweet for tweet in tweets]
   count_tweets = 0
   #timezone of your variable
   from_zone = tz.gettz('UTC')
   #timezone you want to convert
   to_zone = tz.gettz(config.local_timezone)

   #iterate the Tweet in tweets_list
   for tweet in tweets_list:
      #tweet author
      tweet_username = tweet.user.screen_name

      #tweet date
      tweet_date = tweet.created_at

      #convert time zone from UTC to GMT+7
      tweet_date = convert_timezone(from_zone, to_zone, tweet_date)

      #get tweet text
      try:
         tweet_text = tweet.retweeted_status.full_text
      except AttributeError:
         tweet_text = tweet.full_text
      
      #create tweet object
      tweet_object = {
         'username' : tweet_username, 
         'date' : tweet_date, 
         'text' : tweet_text}
      print(tweet_object)

      #insert to database
      # insert_database(tweet_object, mycol)

      #count Tweet that is inserted
      count_tweets+=1

   finish_text = 'total twitter : %d'%count_tweets
   return finish_text

print(search_twiter(connect_twitter()))