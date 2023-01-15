#import file
import config #contain configuration of the application
import tweepy_task
import database_action

#import library
import tweepy     #use for twitter scrapping
# import pymongo    #use for connecting to mongodb
from dateutil import tz #use for timezone converting
import datetime   #use for timezone converting

#you can edit mongodb server, database name, collection name in file name "config.py"
db_action = database_action.DatabaseAction()

#scrap twitter data from Twitter API
class PullTwitterData(object):

   #initialize variable
   def __init__(self, tweets_list=[], count_tweets=0):
      self.tweets_list = tweets_list
      self.count_tweets = count_tweets

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
   
   def database_decision(self, id, username, date, time, text, fav_count, retweet_count):
      
      collection = db_action.tweetdb_object(
         config.mongo_client,
         config.database_name,
         config.collection_name
      )

      cursor = db_action.tweetdb_find(config.collection_name, collection, "id", id)

      db_action.not_print_raw()

      #if found then update data
      if list(cursor) != []:
         data_field = ['favorite_count', 'retweet_count']
         data_list = [fav_count, retweet_count]
         dict_to_update = db_action.tweetdb_create_object(data_field,data_list)

         db_action.tweetdb_update(config.collection_name, collection, dict_to_update, "id", id)

         # print('Update ID :', id)

         #count tweets that are updated
         self.count_tweets+=1
            
      else:
         data_field = ['id', 'username', 'date', 'time', 'text', 'favorite_count', 'retweet_count']
         data_list = [id, username, date, time, text, fav_count, retweet_count]

         dict_to_insert = db_action.tweetdb_create_object(data_field, data_list)

         db_action.tweetdb_insert(config.collection_name, collection, dict_to_insert)

         # print('Insert ID :', id)

         #count Tweet that is inserted
         self.count_tweets+=1
      
      return self.count_tweets
   
   def twitter_scarpping(self, tweets_data):
      #count tweet
      self.count_tweets = 0

      #timezone of your variable
      from_zone = tz.gettz('UTC')
      #timezone you want to convert
      to_zone = tz.gettz(config.local_timezone)

      #iterate the Tweet in tweets_list
      for tweet in self.tweets_list:

         tweet_id = str(tweet.id) #tweet id
         tweet_username = tweet.user.screen_name #tweet author
         tweet_date = tweet.created_at #tweet date
         fav_count = tweet.favorite_count #favorite count
         retweet_count = tweet.retweet_count #retweet count

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

         #connect to database
         db_action.tweetdb_object(
            config.mongo_client,
            config.database_name,
            config.collection_name)
         self.database_decision(tweet_id,tweet_username,tweet_date,tweet_time,tweet_text,fav_count,retweet_count)

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

      print(len(self.tweets_list))

      self.twitter_scarpping(self.tweets_list)

      #finish text for unittest
      finish_text = 'TOTAL TWITTER : %d'%self.count_tweets

      print(finish_text)
   
      return finish_text


if __name__ == '__main__':

   auth = tweepy.OAuth1UserHandler(
      config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
      )
   api = tweepy.API(auth)
   PullTwitterData().search_twitter(api)