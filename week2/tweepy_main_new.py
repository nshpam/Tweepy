import tweepy_search
import twitterDataSentiment
import twitterDataProcessing
#import twitterDataRankings
import config
import datetime
import tweepy
import database_action
import numpy as np

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
        # self.start_date = datetime.date(2022, 12, 30) #y m d
        # self.end_date = datetime.date(2023, 1, 16)
        self.db_action = database_action.DatabaseAction()

    #connect to tweepy
    def ConnectTweepy(self):
        
        auth = tweepy.OAuth1UserHandler(
            config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
            )
        api = tweepy.API(auth)

        return api

    def CheckConsecutive(self, date_list):
        #return True if differences between consecutive numbers
        #which means it's a continuous timeline
        if np.all(np.diff(sorted(date_list))==1):
            return True
        return False
    
    #create checkpoint based-on timelist
    def SetDiscreteCheckPoint(self, date_list):
        #find how many days
        time_delta = len(date_list)

        #even day
        if time_delta%2 == 0:
            interval = time_delta/2
            checkpoint = [interval-1, interval, True]
        #odd day
        else:
            interval = (time_delta-1)/2
            checkpoint = [interval-1, interval+1, False]
        return checkpoint
        
    #create checkpoint based-on timeline
    def SetContinuousCheckPoint(self, start_d, end_d):
        #find how many days
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

    #Check if have this keyword in database
    def IsMatch(self, collection, query_object):
        #keyword not match
        if collection.count_documents(query_object) == 0:
            return False
        #keyword match
        return True

    #get all timeline in the database
    def GetAllTimeline(self, cursor):
        time_list = []
        #get all time in this keyword
        for doc in cursor:
            time_list.append(doc['date'].date())
        
        #remove the repeat time
        time_list = sorted(list(set(time_list)))

        return time_list
    
    def CheckRemain(self, process_date, date_list):
        remain_list = []
        
        #check which date are remain from the process
        for date in date_list:
            if date not in process_date:
                remain_list.append(date)
        
        return remain_list
    
    def NextProcess(self, cur_process):
        if cur_process == 'visualize':
            next_process = 'sentiment'
        elif cur_process == 'sentiment':
            next_process = 'transform'
        elif cur_process == 'transform':
            next_process = 'extract'
        elif cur_process == 'extract':
            next_process = 'pull'
        else:
            return 'Invalid process'
        return next_process

    #check if it's a timeline or a day
    def CheckOneDay(self, start_d, end_d):
        if start_d == end_d:
            return True
        return False

    def CreateDateList(self, start_d, end_d):
        interval = datetime.timedelta(days=1)
        end_d += interval
        time_delta = (end_d - start_d)
        date_list = []
        
        # print(type(time_delta), time_delta.days)

        for i in range(time_delta.days):
            date_list.append(start_d)
            start_d+=interval
        
        return date_list
    
    #always continuous timeline
    #create the date that need to be process
    def CreateTimeline(self, start_d, end_d, checkpoint, time_list, even, cur_process):
        interval = datetime.timedelta(days=1)
        # end_d += interval
        time_delta = (end_d - start_d)
        process_date = []
        data_dict = {}
        cp1 = checkpoint[0]
        cp2 = checkpoint[1]
        date_list = []
        
        print(start_d, end_d)

        #odd number
        if not even:
            cp = checkpoint[0]+interval
            date_list.append(cp)
            #check the first checkpoint
            if cp not in time_list :
                process_date.append(cp)
            
        while True:
            
            #cp1 meet the start point, cp2 meet the end point
            if cp1 == start_d-interval or cp2 == end_d+interval:
                break
            date_list.append(cp1)
            date_list.append(cp2)
            #check checkpoint 1
            if cp1 not in time_list:
                process_date.append(cp1)
            cp1 -= interval
            #check checkpoint 2
            if cp2 not in time_list:
                process_date.append(cp2)
            cp2+=interval
        
        data_dict[cur_process] = self.CheckRemain(process_date, date_list)
        data_dict[self.NextProcess(cur_process)] = process_date

        # print('date to sentiment(continuous)',process_date)
        return data_dict

    #continuous timeline
    #check the date that need to be process
    def CheckDBTimeline(self, keyword, start_d, end_d, collection_name, cur_process):
        db_action = self.db_action
        time_list = []
        data_dict = {}
        db_action.not_print_raw() #turn off status printing

        #select the collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, collection_name)
        query_object_1 = db_action.tweetdb_create_object(['keyword'],[keyword])
        cursor = db_action.tweetdb_find(collection_name, collection, query_object_1)
        
        #no keyword match
        if not self.IsMatch(collection, query_object_1):
            data_dict[cur_process] = []
            data_dict[self.NextProcess(cur_process)] = self.CreateDateList(start_d, end_d)
            return data_dict
            
        #get all time in this keyword
        time_list = self.GetAllTimeline(cursor)
            
        #one day search
        if self.CheckOneDay(start_d, end_d):
            #no data in this time period
            if start_d not in time_list:
                data_dict[cur_process] = []
                data_dict[self.NextProcess(cur_process)] = [start_d]
            else:
                data_dict[cur_process] = [start_d]
                data_dict[self.NextProcess(cur_process)] = []

        #period day search
        else:
            #create a checkpoint
            checkpoint = self.SetContinuousCheckPoint(start_d, end_d)
            #contain the data that identify odd day / even day already
            data_dict = self.CreateTimeline(start_d, end_d, checkpoint, time_list, checkpoint[2], cur_process)
            
        return data_dict

    #either continuous timeline or discrete timeline
    #create the date that need to be process
    def CreateTimelist(self, date_list, checkpoint, time_list, even, cur_process):
        interval = 1
        time_delta = len(date_list)
        process_date = []
        cp1 = checkpoint[0]
        cp2 = checkpoint[1]

        data_dict = {}

        #odd number
        if not even:
            cp = time_delta/2
            #check the first checkpoint
            if date_list[cp] not in time_list:
                process_date.append(cp)

        while True:
            #cp1 meet the start point, cp2 meet the end point
            if date_list[cp1] == 0 or date_list[cp2] == time_delta-1:
                break
            #check checkpoint 1
            if date_list[cp1] not in time_list:
                process_date.append(date_list[cp1])
            cp1 -= interval
            #check checkpoint 2
            if date_list[cp2] not in time_list:
                process_date.append(date_list[cp2])
            cp2 += interval

        data_dict[cur_process] = self.CheckRemain(process_date, date_list)
        data_dict[self.NextProcess(cur_process)] = process_date

        return data_dict
    
    #discrete timeline or continuous timeline
    #create the date that need to be process
    def CheckDBTimelist(self, keyword, date_list, collection_name, cur_process):
        db_action  = self.db_action
        time_list = []
        data_dict = {}
        db_action.not_print_raw() #turn off status printing

        #select the collection
        collection = db_action.tweetdb_object(db_action.tweetdb_object(config.mongo_client, config.database_name, collection_name))
        query_object_1 = db_action.tweetdb_create_object(['keyword'],[keyword])
        cursor_1 = db_action.tweetdb_find(collection_name, collection, query_object_1)
        
        #keyword doesn't exists
        if not self.IsMatch(collection, query_object_1):
            data_dict[cur_process] = []
            data_dict[self.NextProcess(cur_process)] = date_list
            return data_dict

        #get all time in this keyword
        time_list = self.GetAllTimeline(cursor_1)

        #one day search
        if self.CheckOneDay(date_list[0], date_list[-1]):
            if date_list[0] not in time_list:
                data_dict[cur_process] = []
                data_dict[self.NextProcess(cur_process)] = [date_list[0]]
            else:
                data_dict[cur_process] = [date_list[0]]
                data_dict[self.NextProcess(cur_process)] = []
        else:
            #create a checkpoint
            #return index of the date
            checkpoint = self.SetDiscreteCheckPoint(date_list)
            #contain the data that identify odd day / even day already
            data_dict = self.CreateTimelist(date_list, checkpoint, time_list, checkpoint[2], cur_process)
        return data_dict

    #can only extract 7 days ago period
    def Extract(self, keyword):

        #connect to tweepy
        api = self.ConnectTweepy()

        #search by keyword
        tweepy_search.PullTwitterData().search_twitter(api, keyword, self.search_type, self.search_limit)

    #transform by keyword (# or word)
    #transform by time

    def SentimentByKeyword(self, keyword):
        db_action = self.db_action
        #sentiment
        sentiment = twitterDataSentiment.SentimentAnalysis()
        data_dict = sentiment.Perform(keyword, [], 'keyword')

        #keyword not match in sentiment database
        if data_dict['sentiment'] == []:
            return data_dict['transform']
        
        #collect sentiment data
        sentiment_data = list(data_dict['sentiment'].values())
        
        db_action.not_print_raw() #turn off printing database status

        #insert data to sentiment database
        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)
        
        #create data object
        data_field = ['id', 'keyword', 'date', 'input', 'score', 'polar', 'conclusion']
        for data in sentiment_data:
            data_list = [data[0], data[1], datetime.datetime.combine(data[2], datetime.time.min), data[3], data[4], data[5], data[6]]
            query_object = db_action.tweetdb_create_object(data_field, data_list)
            
            #check duplicate data before insertion
            check_query = db_action.tweetdb_create_object(["id"],[data[0]])
            
            if not self.IsMatch(collection, check_query):
                db_action.tweetdb_insert(config.collection_name_5, collection, query_object)
        
        return data_dict['transform']
        

    #sentiment by time
    def SentimentByTime(self, keyword, start_d, end_d):
        process_date = []
        data_dict = {}
        db_action = self.db_action

        #check sentiment database
        #return only the date that need to be sentiment
        #always continuous timeline
        sentiment_date = self.CheckDBTimeline(keyword, start_d, end_d, config.collection_name_5, 'visualize')

        if sentiment_date['visualize'] != [] and sentiment_date['sentiment'] == []:
            return 'show data visualization'
        #perform sentiment
        elif sentiment_date['sentiment'] != []:
            #sort the date
            process_date = sorted(sentiment_date['sentiment'])
           
            #sentiment
            sentiment = twitterDataSentiment.SentimentAnalysis()
            data_dict = sentiment.Perform(keyword, process_date, 'time')

            if data_dict['sentiment'] == []:
                return data_dict['transform']

            sentiment_data = list(data_dict['sentiment'].values())
            
            #insert data to sentiment database
            #create collection
            collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)
            #create data object
            data_field = ['id','keyword', 'date', 'input', 'score', 'polar', 'conclusion']
            for data in sentiment_data:
                date_list = [data[0], data[1], datetime.datetime.combine(data[2], datetime.time.min), data[3], data[4], data[5], data[6]]
                query_object = db_action.tweetdb_create_object(data_field, date_list)

                #check duplicate data before insertion
                check_query = db_action.tweetdb_create_object(["id"],[data[0]])
                
                if not self.IsMatch(collection, check_query):
                    db_action.tweetdb_insert(config.collection_name_5, collection, query_object)

            return data_dict['transform']
        else:
            return 'Invalid response'

        #check if sentiment this keyword on this period
        #check timeline type
        #check if transformed this keyword on this period
        #check if extract this keyword on this period

    def TransformByKeyword(self, keyword):
        db_action = self.db_action

        #transform
        tokenization = twitterDataProcessing.Tokenization()
        tokenization_dict = tokenization.Perform(keyword, [], 'keyword')

        #keyword not match in transform database
        #no cleaning, normalize
        if tokenization_dict['transform'] == []:
            return tokenization_dict['extract']
        
        #collect tokenize data
        tokenize_data = list(tokenization_dict['transform'].values())
        
        #perform normalization process
        normalize = twitterDataProcessing.Normailize()
        normalize_dict = normalize.Perform(tokenize_data)
        #collect normalize data
        normalize_data = list(normalize_dict['transform'].values())

        #perform cleaning process
        cleaning = twitterDataProcessing.CleanThaiAndEng()
        cleaned_dict = cleaning.Perform(normalize_data)

        transform_data = list(cleaned_dict['transform'].values())

        data_dict = cleaned_dict
        
        db_action.not_print_raw() #turn off printing database status

        #insert data to sentiment database
        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)

        #create data object
        data_field = ['id', 'keyword', 'date', 'text']
        for data in transform_data:
            data_list = [data[0], data[1], datetime.datetime.combine(data[2], datetime.time.min), data[3]]
            query_object = db_action.tweetdb_create_object(data_field, data_list)

            #check duplicate data before insertion
            check_query = db_action.tweetdb_create_object(["id"],[data[0]])

            if not self.IsMatch(collection, check_query):
                # print('insert')
                db_action.tweetdb_insert(config.collection_name_2, collection, query_object)

            print(query_object)

        return data_dict['extract']

    def TransformByTime(self, keyword, date_list):
        process_date = sorted(date_list) #sort date
        data_dict = {}
        db_action = self.db_action
        
        #check timeline type
        #continuous timeline
        if self.CheckConsecutive(date_list):
            transform_date = self.CheckDBTimeline(keyword, date_list[0], date_list[-1], config.collection_name_2, 'sentiment')
        else:
            transform_date = self.CheckDBTimelist(keyword, date_list, config.collection_name_2, 'sentiment')
        
        #keyword not match
        if transform_date == None:
            return 'keyword not match'
        #all data has been transformed ready to sentiment
        elif transform_date['sentiment'] != []:
            return 'sentiment'
        elif transform_date['transform'] != []:
            #transform
            pass
        else:
            return 'Invalid response'

if __name__ == '__main__':
    mainoperation = MainOperation()

    start_date = datetime.date(2023, 1, 14) #y m d
    # end_date = datetime.date(2023, 1, 15)
    end_date = datetime.date(2023, 1, 16)
    
    transform = mainoperation.SentimentByKeyword(config.search_word)
    # transform = mainoperation.SentimentByTime(config.search_word, start_date, end_date)
    
    print('transform', transform)

    extract = mainoperation.TransformByKeyword(config.search_word)

    print('extract', extract)