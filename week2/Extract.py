#import file
import config
import database_action
import tweepy
from dateutil import tz
import datetime
from twitterDataProcessing import FilterData, Tokenization

db_action = database_action.DatabaseAction()

class ExtractTwitter():

    #connect to tweepy API
    def ConnectTweepy(self):
        auth = tweepy.OAuth1UserHandler(config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret)
        return tweepy.API(auth)

    def SearchTwitter(self, keyword, settings):
        #collect settings data
        search_type = settings['search_type']
        num_tweet = settings['num_tweet']

        #connect to tweepy API
        api = self.ConnectTweepy()

        #user cursor to search
        try:
            tweets = tweepy.Cursor(
         api.search_tweets ,
         q=keyword + ' -filter:retweets', 
         tweet_mode=config.search_mode,
         result_type=search_type
         ).items(num_tweet)
        except:
            return 'Too many Requests. Rate limit exceeded. Wait 15 minutes and try again'
        
        # create a list of Tweets
        tweets_list = [tweet for tweet in tweets]

        return tweets_list

    def SettingTimeZone(self):
        #timezone of your data
        from_zone = tz.gettz('UTC')
        #timezone you want to convert
        #Thailand/Bangkok
        to_zone = tz.gettz(config.local_timezone)
        return {'from_zone': from_zone, 'to_zone': to_zone}
    
    #convert timezone from UTC to GMT
    def ConvertTimezone(self, from_zone, to_zone, convert_date):
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
        convert_date = convert_date.replace(tzinfo=from_zone).astimezone(to_zone)
        return convert_date

    
    def GetTweetLocation(self, place):
        if place != None:
            return place.bounding_box.coordinates[0][0]
        return None

    def GetTweetText(self, tweet):
        try:
            tweet_text = tweet.retweeted_status.full_text
        except:
            tweet_text = tweet.full_text
        return tweet_text

    def Perform(self, keyword, tweet_data):
        #timezone settings
        tz_settings = self.SettingTimeZone()
        data_dict = {}

        #iterate the Tweet in tweets list
        for tweet in tweet_data:
            
            #extracting tweet data
            tweet_id = tweet.id #tweet id
            tweet_username = tweet.user.screen_name #tweet author
            tweet_date = self.ConvertTimezone(tz_settings['from_zone'], tz_settings['to_zone'], tweet.created_at) #tweet date
            fav_count = tweet.favorite_count #favorite count
            retweet_count = tweet.retweet_count #retweet count
            tweet_location = self.GetTweetLocation(tweet.place) #get tweet location
            tweet_text = self.GetTweetText(tweet) #get tweet text

            #create object for insertion
            data_field = ['id', 'keyword', 'username', 'date', 'location', 'text', 'favorite_count', 'retweet_count']
            data_list = [tweet_id, keyword, tweet_username, tweet_date, tweet_location, tweet_text, fav_count, retweet_count]
            db_action.not_print_raw()
            
            #collect data
            data_dict[tweet_id] = db_action.tweetdb_create_object(data_field, data_list)
        return data_dict

if __name__ == '__main__':
    extract = ExtractTwitter()
    settings = {
        'search_type' : config.search_type,
        'num_tweet' : config.num_tweet
    }
    tweet_list = extract.SearchTwitter(config.search_word, settings)
    tweet_dict = extract.Perform(config.search_word, tweet_list)
    # extract.DuplicateFilter(config.search_word, tweet_dict)
    print(len(list(tweet_dict.keys())))
    # print(tweet_dict)

