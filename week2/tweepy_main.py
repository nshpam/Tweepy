import tweepy_search
import twitterDataSentiment
import twitterDataProcessing
import twitterDataRankings
import config
import datetime
import tweepy
import database_action

class MainOperation():

    #collect user interaction
    def __init__(self, keyword='', search_type='', search_limit=0, start_date=None, end_date=None, db_action=None):

        self.keyword = keyword
        self.search_type = search_type
        self.search_limit = search_limit
        self.start_date = start_date
        self.end_date = end_date
        self.db_action = db_action

        self.keyword = config.search_word
        self.search_type = config.search_type
        self.search_limit = config.num_tweet
        self.start_date = datetime.date(2022, 12, 30) #y m d
        self.end_date = datetime.date(2023, 1, 16)
        self.db_action = database_action.DatabaseAction()

    #extract and load twitter data
    def Extract(self, keyword):
        print('Extract begin...')
        
        #connect to tweepy
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
            )
        api = tweepy.API(auth)
        
        #search by keyword
        tweepy_search.PullTwitterData().search_twitter(api, keyword, self.search_type, self.search_limit)

        print('Extract end...')
    
    #transform
    def check_previous(self, previous, time_list):
        if previous not in time_list:
            return False #True = perform transformation
        return True

    def check_next(self, next, time_list):
        if next not in time_list:
            return False #True = perform transformation
        return True
    
    def set_scope(self, checkpoint, end_d):
        if checkpoint > end_d:
            return end_d
        return checkpoint
    
    def transform_one_day(self, day, time_list):
        if day in time_list:
            return []
        return [day]

    def transform_period(self, checkpoint, end_d, time_list, interval):

        tf_date_list = []
        while checkpoint <= end_d:

            previous = self.set_scope(checkpoint, end_d)
            next = self.set_scope(checkpoint, end_d)
            
            #check checkpoint
            if checkpoint not in time_list:
                print('transform')
                tf_date_list.append(checkpoint)
            
            #check previous and next
            for i in range(1,8):
                #previous
                previous -= interval
                if not self.check_previous(previous, time_list):
                    tf_date_list.append(previous)
                    # print('perform transformation')

                #next
                next -= interval
                if not self.check_next(next, time_list):
                    tf_date_list.append(next)
                    # print('perform transformation')
            
            #pin new checkpoint
            checkpoint += datetime.timedelta(days=14)
        
        return tf_date_list

    def check_tf_timeline(self, checkpoint, end_d, time_list):
        interval = datetime.timedelta(days=1)
        #check if it's a period or it's a day
        if checkpoint == end_d:
            #transform one day
            return self.transform_one_day(checkpoint, time_list)
        #transform period
        return self.transform_period(checkpoint, end_d, time_list, interval)
            
    def CheckCleanedDB(self, start_d, end_d):
        db_action = self.db_action
        time_list = []
        collection_2 = db_action.tweetdb_object(
            config.mongo_client,
            config.database_name,
            config.collection_name_2
        ) 

        query_object_2 = db_action.tweetdb_create_object(["_id","date"],[0,1])
        cursor_2 = db_action.tweetdb_show_collection(config.collection_name_2, collection_2, query_object_2)
        
        #pull date and time from cleaned database
        for doc in cursor_2:
            time_list.append(doc['date'].date())
        time_list = sorted(list(set(time_list)))

        result = sorted(list(set(self.check_tf_timeline(start_d, end_d, time_list))))
        
        print('data in database :',time_list)
        print('tf_date_list :',result)

        return result

    def TransformByTime(self, tf_date_list):
        tweet_dict = twitterDataProcessing.Tokenization().LextoPlusTokenization(
                config.LextoPlus_API_key, config.LextoPlus_URL, config.search_word, tf_date_list
            )

        tweet_dict_keys = list(tweet_dict.keys())
        tweet_dict_values = list(tweet_dict.values())
        twitterDataProcessing.Transform().perform(tweet_dict_keys, tweet_dict_values)

    #Transform and load tweets data
    def TransformByTime_old(self):
        #check if the data should be transformed
        tf_date_list = self.CheckCleanedDB(self.start_date, self.end_date)
        #if it transform already so we skip them
        if tf_date_list == []:
            print('there is nothing to transform')
            print('sentiment')
        #if not perform the transformation or extract
        #extract commander should be sentiment function
        #if have data but not transform yet
        else:
            #transform by time
            tweet_dict = twitterDataProcessing.Tokenization().LextoPlusTokenization(
                config.LextoPlus_API_key, config.LextoPlus_URL, config.search_word, tf_date_list
            )

            tweet_dict_keys = list(tweet_dict.keys())
            tweet_dict_values = list(tweet_dict.values())
            twitterDataProcessing.Transform().perform(tweet_dict_keys, tweet_dict_values)
    
    def TransformByKeyword(self):
        tweet_dict = twitterDataProcessing.Tokenization().LextoPlusTokenization(
                config.LextoPlus_API_key, config.LextoPlus_URL, config.search_word, ['keyword']
            )

        tweet_dict_keys = list(tweet_dict.keys())
        tweet_dict_values = list(tweet_dict.values())
        twitterDataProcessing.Transform().perform(tweet_dict_keys, tweet_dict_values)

    #Sentiment
    def SetCheckPoint(self, start_d, end_d):
        #check time
        time_delta = (end_d - start_d)+ datetime.timedelta(days=1)
        
        #even day
        if time_delta.days %2 == 0:
            interval = datetime.timedelta(days=int(time_delta.days/2)-1)
            checkpoint = [start_d+interval, end_d-interval, True]
            
        #odd day
        else:
            interval = datetime.timedelta(days=int((time_delta.days-1)/2))
            cp_interval = datetime.timedelta(days=1)
            cp = end_d-interval
            checkpoint = [cp-cp_interval, cp+cp_interval, False]

        return checkpoint
    
    def CheckTimeline(self, start_d, end_d, checkpoint, time_list, even):

        interval = datetime.timedelta(days=1)
        end_d += interval
        time_delta = (end_d - start_d)
        process_date = []
        cp1 = checkpoint[0]
        cp2 = checkpoint[1]
        
        print(start_d, end_d)

        #odd number
        if not even:
            cp = end_d-time_delta
            #check the first checkpoint
            if cp not in time_list :
                process_date.append(cp)
            
        while True:
            #check checkpoint 1
            if cp1 == start_d-interval or cp2 == end_d+interval:
                break
            if cp1 not in time_list:
                process_date.append(cp1)
            cp1 -= interval
            #check checkpoint 2
            if cp2 not in time_list:
                process_date.append(cp2)
            cp2+=interval

        print('date to sentiment',process_date)
        return process_date

    def CheckSentimentDB(self, start_d, end_d):
        db_action = self.db_action
        time_list = []
        sentiment_date = []
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)

        db_action.not_print_raw()
        
        query_object = db_action.tweetdb_create_object(["_id", "date"], [0,1])
        cursor = db_action.tweetdb_show_collection(config.collection_name_5, collection, query_object)

        #pull time from sentiment database
        for doc in cursor:
            time_list.append(doc['date'].date())
        
        checkpoint = self.SetCheckPoint(start_d, end_d)

        if start_d == end_d:
            if start_date not in time_list:
                sentiment_date = [start_date]
        else:
            #even day
            if checkpoint[2]:
                sentiment_date = self.CheckTimeline(start_d, end_d, checkpoint, time_list, checkpoint[2])
            #odd day
            else:
                sentiment_date = self.CheckTimeline(start_d, end_d, checkpoint, time_list, checkpoint[2])
        
        return sentiment_date

    def SentimentByTime(self, start_d, end_d):
        sentiment_date = self.CheckSentimentDB(start_d, end_d)

        if sentiment_date == []:
            #show sentiment data visualization
            print('show data visualization')
        else:
            #case 1 :have data but not sentiment
            #case 2 :don't have data to sentiment
            #both case need to check cleaned database

            #check if the datae exist and collect data
            sentiment_date = sorted(sentiment_date)
            self.CheckCleanedDB(sentiment_date[0], sentiment_date[-1])
            pass
    
    def SentimentByKeyword(self):
        pass

    # def CheckCleanedDB(self, date_list):
    #     #if have all the cleaned data then return it
    #     #if not pull data from tweets and clean
    #     pass

    def CheckTweetsDB(self, date_list):
        #if have all the tweet data then return it
        #if not pull data from tweet
        #if no tweet in that period show error
        pass

    def CheckSearchMode(self, mode, date_list=[]):
        if mode == 'keyword':
            #sentiment by keyword
            pass
        elif mode == 'time':
            #sentiment by time
            #check sentiment database
            self.CheckTimeline(date_list)
            pass
        else:
            return 'Invalid Mode'
    

if __name__ == '__main__':
    # MainOperation().ExtractAndLoad(config.search_word)
    # MainOperation().Transform()

    mainoperation = MainOperation()

    start_date = datetime.date(2022, 12, 30) #y m d
    # end_date = datetime.date(2023, 1, 15)
    end_date = datetime.date(2023, 1, 16)

    mainoperation.CheckTimeline(start_date, end_date)