#import file
import config #contain configuration of the application
import tweepy_task
import database_action

#import library
import tweepy     #use for twitter scrapping
# import pymongo    #use for connecting to mongodb
from dateutil import tz #use for timezone converting
import datetime   #use for timezone converting
import twitterDataProcessing

# from GUI_main import *
#you can edit mongodb server, database name, collection name in file name "config.py"
db_action = database_action.DatabaseAction()

#scrap twitter data from Twitter API
class PullTwitterData(object):

   #initialize variable
   def __init__(self, tweets_list=[], count_tweets=0, count_duplicate=0, filters=twitterDataProcessing.FilterData()):
      self.tweets_list = tweets_list
      self.count_tweets = count_tweets
      self.count_duplicate = count_duplicate
      self.filters = filters

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
      # convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone).strftime('%d-%m-%Y | %H:%M')
      convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone)
      return convert_date

   def pull_all_data(self, cursor):

      all_data = []

      for doc in cursor:
         raw_list = doc['text'].split()
         clean_data = ''
         for word in raw_list:
            if not self.filters.FilterUrl(word):
               clean_data += word
         all_data.append(clean_data)
      
      return all_data

   def check_duplicate(self, text, cursor):
      raw_list = text.split()
      clean_data = ''
      
      for word in raw_list:
         if not self.filters.FilterUrl(word):
            clean_data += word
      
      if clean_data in self.pull_all_data(cursor):
         return True
      return False
   
   def database_decision(self, id, username, date, text, fav_count, retweet_count, location, keyword):
      
      collection = db_action.tweetdb_object(
         config.mongo_client,
         config.database_name,
         config.collection_name
      )

      data_field = ["_id", "id", "text"]
      data_list = [0, 1, 1]
      
      query_object_1 = db_action.tweetdb_create_object(["id"],[id])
      query_object_2 = db_action.tweetdb_create_object(["text"],[1])

      #find object using id
      cursor_1 = db_action.tweetdb_find(config.collection_name, collection, query_object_1)
      cursor_2 = db_action.tweetdb_show_collection(config.collection_name, collection, query_object_2)

      db_action.not_print_raw()

      #if found then update data
      if list(cursor_1) != []:
         data_field = ['favorite_count', 'retweet_count']
         data_list = [fav_count, retweet_count]
         dict_to_update = db_action.tweetdb_create_object(data_field,data_list)

         db_action.tweetdb_update(config.collection_name, collection, dict_to_update, "id", id)

         #count tweets that are updated
         self.count_tweets+=1
      
      #if different unique id but same content
      if self.check_duplicate(text, cursor_2):
         self.count_tweets+=1
         self.count_duplicate += 1
         # print('data duplicate :', text)

      #if not then insert
      else:

         data_field = ['id', 'keyword', 'username', 'date', 'location', 'text', 'favorite_count', 'retweet_count']
         data_list = [id, keyword, username, date, location, text, fav_count, retweet_count]

         dict_to_insert = db_action.tweetdb_create_object(data_field, data_list)

         db_action.tweetdb_insert(config.collection_name, collection, dict_to_insert)

         #count Tweet that is inserted
         self.count_tweets+=1
      
      return self.count_tweets
   
   def twitter_scrapping(self, tweet_data, tweet_keyword):
      #count tweet
      self.count_tweets = 0

      #timezone of your variable
      from_zone = tz.gettz('UTC')
      #timezone you want to convert
      to_zone = tz.gettz(config.local_timezone)

      #iterate the Tweet in tweets_list
      for tweet in tweet_data:

         tweet_id = tweet.id #tweet id
         tweet_username = tweet.user.screen_name #tweet author
         tweet_date = tweet.created_at #tweet date
         fav_count = tweet.favorite_count #favorite count
         retweet_count = tweet.retweet_count #retweet count

         #get tweet location
         if tweet.place is not None:
            tweet_location = tweet.place.full_name
         else:
            tweet_location = None

         #get tweet text
         try:
            tweet_text = tweet.retweeted_status.full_text
         except AttributeError:
            tweet_text = tweet.full_text

         #convert time zone from UTC to GMT+7
         #format the date
         tweet_date = self.convert_timezone(from_zone, to_zone, tweet_date)

         #connect to database
         db_action.tweetdb_object(
            config.mongo_client,
            config.database_name,
            config.collection_name)
         self.database_decision(tweet_id,tweet_username,tweet_date,tweet_text,fav_count,retweet_count,tweet_location,tweet_keyword)

   #scarp twitter
   def search_twitter(self, api, keyword, search_type, num_tweet):

      #use Cursor to serach
      #tweepy.Cursor(search API, word + filter, search mode, search type).items(search limit)
      tweets = tweepy.Cursor(
         api.search_tweets ,
         q=keyword + ' -filter:retweets', 
         tweet_mode=config.search_mode,
         result_type=search_type
         ).items(num_tweet)

      #create a list of Tweets
      self.tweets_list = [tweet for tweet in tweets]

      print(len(self.tweets_list))

      self.twitter_scrapping(self.tweets_list, keyword)

      #finish text for unittest
      finish_text = 'TOTAL TWITTER : %d'%self.count_tweets
      duplicate_text = 'TOTAL DUPLICATE: %d'%self.count_duplicate

      print(finish_text)
      print(duplicate_text)
   
      return finish_text
   
   def pull_trends(self, api, woeid, ranking_top):
      trends = api.get_place_trends(woeid)
      trends_list = trends[0]['trends'][:ranking_top]
      trends_keyword = []

      for trend in trends_list:
         temp_dict = {}
         print(trend['name'], trend['tweet_volume'])
            
         # if trend['name'][0] != '#':
         #    trend['name'] = '#' + trend['name']

         temp_dict[trend['name']] = trend['tweet_volume']
         trends_keyword.append(temp_dict)
      return trends_keyword

   def pull_trends_hashtags(self, api, woeid):
      trends = api.get_place_trends(woeid)
      trends_list = trends[0]['trends']
      trends_hashtags = []
      trends_dict = []

      for trend in trends_list:
         if trend['name'][0] == '#' and len(trends_hashtags) < 10:
               trends_hashtags.append(trend['name'])
               temp_dict = {trend['name']: trend['tweet_volume']}
               trends_dict.append(temp_dict)
         if len(trends_hashtags) == 10:
            break

      return trends_dict

   def pull_trends_word(self, api, woeid):
      trends = api.get_place_trends(woeid)
      trends_list = trends[0]['trends']
      trends_word = []
      trends_dict = []

      for trend in trends_list:
         if trend['name'][0] != '#' and len(trends_word) < 10:
               trends_word.append(trend['name'])
               temp_dict = {trend['name']: trend['tweet_volume']}
               trends_dict.append(temp_dict)

         if len(trends_word) == 10:
               break
      return trends_dict

      

# if __name__ == '__main__':

   # auth = tweepy.OAuth1UserHandler(
   #    config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
   #    )
   # api = tweepy.API(auth)
#    #search by keyword
#    PullTwitterData().search_twitter(api, config.search_word)

   #search by trends
   # trends_keyword = PullTwitterData().pull_trends(api, config.WOEid, config.ranking_top)
   # for trend in range

   # print(trends_keyword)