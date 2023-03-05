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
            
    def check_tf(self, start_d, end_d):
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
    
    def Sentiment(self):
        #sentiment
        pass

    #Transform and load tweets data
    def TransformByTime(self):
        #check if the data should be transformed
        tf_date_list = self.check_tf(self.start_date, self.end_date)
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
    
    def SetCheckPoint(self, start_d, end_d):
        #check time
        time_delta = (end_d - start_d)+ datetime.timedelta(days=1)
        interval_1 = datetime.timedelta(days=int(time_delta.days/2))
        interval_2 = datetime.timedelta(days=int(time_delta.days/2-1))
        print(time_delta.days)
        print(start_d, end_d)
        #even day
        if time_delta.days %2 == 0:
            checkpoint = [end_d-interval_1, end_d-interval_2]
        #odd day
        else:
            checkpoint = [end_d-interval_1]
        return checkpoint
    
    def CheckSentimentTimeline(self, start_d, end_d, checkpoint, time_list, even):

        interval = datetime.timedelta(days=1)
        time_delta = (end_d - start_d)+ interval
        date_sentiment = []
        
        if even == True:
            checkpoint_s = checkpoint[0]
            checkpoint_e = checkpoint[1]
            for i in range(int(time_delta.days/2)):
                print(checkpoint_s, checkpoint_s not in time_list)
                print(checkpoint_e, checkpoint_e not in time_list)
                #check checkpoint 1 (start)
                if checkpoint_s not in time_list:
                    date_sentiment.append(checkpoint_s)
                checkpoint_s -= interval
                if checkpoint_e not in time_list:
                    date_sentiment.append(checkpoint_e)
                checkpoint_e += interval
        else:
            checkpoint = checkpoint[0]
            for i in range(int(time_delta.days/2)):
               pass

        print('date to sentiment',date_sentiment)

                #check checkpoint 2 (end)



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
        print(checkpoint)

        #even day
        if len(checkpoint) == 2:
            self.CheckSentimentTimeline(start_d, end_d, checkpoint, time_list, True)
        #odd day
        else:
            pass
        

    def CheckCleanedDB(self, date_list):
        pass

    def CheckTweetsDB(self, date_list):
        pass

    #extract by time
    def PerformSentimentByTime(self):
        #check sentiment database

        #check cleaned database

        #check tweets database

        #check if that timeline in tweets database
        #check if the correction of timeline
        #extract

        #check if that timeline transformed already
        #chcek if the correction of timeline
        #transform
        #sentiment
        #show report page (total extract, keyword, sentiment score, top 10 word, date range, pie chart sentiment, sentiment top 10 word)
        #show data visualization of sentiment
        #show ranking
        pass

    #extract by keyword
    def PerformSentimentByKeyword(self):
        pass

if __name__ == '__main__':
    # MainOperation().ExtractAndLoad(config.search_word)
    # MainOperation().Transform()

    mainoperation = MainOperation()

    start_date = datetime.date(2022, 12, 30) #y m d
    end_date = datetime.date(2023, 1, 16)

    mainoperation.CheckSentimentDB(start_date, end_date)