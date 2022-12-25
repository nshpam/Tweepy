import tweepy
import pymongo
from dateutil import tz
import config

#connect to database
myclient = pymongo.MongoClient(config.mongo_client)
mydb = myclient[config.database_name]
mycol = mydb[config.collection_name]

def convert_timezone(from_zone, to_zone, convert_date):
   #fixed time zone
   convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%d-%m-%Y | %H:%M')
   return convert_date

def insert_database(data, collection_variable):
   cmd = collection_variable.insert_one(data)
   return cmd

#connect to twitter
def connect_twitter():
   auth = tweepy.OAuth1UserHandler(
      config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
   )
   api = tweepy.API(auth)
   return api

def search_twiter(api):

   #use Cursor to serach
   tweets = tweepy.Cursor(
      api.search_tweets ,
      q=config.search_word + ' -filter:retweets', 
      # lang=config.search_lang,
      tweet_mode=config.search_mode
      # result_type=config.search_type
      ).items(config.num_tweet)

   tweets_list = [tweet for tweet in tweets]
   count_tweets = 0
   from_zone = tz.gettz('UTC')
   to_zone = tz.gettz(config.local_timezone)

   for tweet in tweets_list:
      #tweet author
      tweet_username = tweet.user.screen_name

      #the unique identifier of the requested Tweet
      tweet_id = tweet.id

      #tweet date
      tweet_date = tweet.created_at

      #convert time zone from UTC to GMT+7
      tweet_date = convert_timezone(from_zone, to_zone, tweet_date)

      #tweet text
      try:
         tweet_text = tweet.retweeted_status.full_text
      except AttributeError:
         tweet_text = tweet.full_text
      
      tweet_object = {
         'username' : tweet_username, 
         'date' : tweet_date, 
         'text' : tweet_text}
      print(tweet_object)

      #insert to database
      # insert_database(tweet_object, mycol)
      count_tweets+=1

   finish_text = 'total twitter : %d'%count_tweets
   return finish_text

print(search_twiter(connect_twitter()))