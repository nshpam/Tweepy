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
        self.start_date = datetime.date(2023, 1, 16)
        # self.start_date = datetime.date(2022, 12, 30) #y m d
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

    def transform_one_day(self):
        pass

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
    
    def check_day(self, start_d, end_d, time_list, interval):
        if start_d == end_d:
            #transform one day
            return self.transform_one_day()
        #transform period
        return self.transform_period(start_d, end_d, time_list, interval)

    def check_tf_timeline(self, checkpoint, end_d, time_list):
        interval = datetime.timedelta(days=1)

        #check if only one day or period
        tf_date_list=self.check_day(self, checkpoint, end_d, time_list, interval)
        
        return tf_date_list
            

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

        print('tf_date_list :',result)

        return result

    #Transform and load tweets data
    def Transform(self):
        #check if the data should be transformed
        tf_date_list = self.check_tf(self.start_date, self.end_date)
        #if it transform already so we skip them
        if tf_date_list == []:
            print('sentiment')
        #if not perform the transformation or extract
        #extract commander should be sentiment function
        else:
            print('transform')
    
    def Sentiment(self):
        #sentiment
        pass

    #press extract button
    def Perform(self):
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

if __name__ == '__main__':
    # MainOperation().ExtractAndLoad(config.search_word)
    MainOperation().Transform()