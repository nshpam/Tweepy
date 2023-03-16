import tweepy_search
import twitterDataSentiment
#import twitterDataProcessing
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
        self.start_date = datetime.date(2022, 12, 30) #y m d
        self.end_date = datetime.date(2023, 1, 16)
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

    #check if the keyword exists in the collection
    def CheckKeyword(self, cursor):

        #keyword exists
        if cursor.count()>0:
            return True
        #keyword doesn't exists
        return False

    #get all timeline in the database
    def GetAllTimeline(self, cursor):
        time_list = []
        #get all time in this keyword
        for doc in cursor:
            time_list.append(doc['date'].date())
        
        #remove the repeat time
        time_list = sorted(list(set(time_list)))

        return time_list
    
    #check if it's a timeline or a day
    def CheckOneDay(self, start_d, end_d):
        if start_d == end_d:
            return True
        return False
    
    #always continuous timeline
    #create the date that need to be process
    def CreateTimeline(self, start_d, end_d, checkpoint, time_list, even):
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
            #cp1 meet the start point, cp2 meet the end point
            if cp1 == start_d-interval or cp2 == end_d+interval:
                break
            #check checkpoint 1
            if cp1 not in time_list:
                process_date.append(cp1)
            cp1 -= interval
            #check checkpoint 2
            if cp2 not in time_list:
                process_date.append(cp2)
            cp2+=interval

        print('date to sentiment(continuous)',process_date)
        return process_date

    #continuous timeline
    #check the date that need to be process
    def CheckDBTimeline(self, keyword, start_d, end_d, collection_name):
        db_action = self.db_action
        time_list = []
        process_date = []
        db_action.not_print_raw() #turn off status printing

        #select the collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, collection_name)
        query_object_1 = db_action.tweetdb_create_object(['keyword'],[keyword])
        cursor_1 = db_action.tweetdb_find(collection_name, collection, query_object_1)

        #keyword exists
        if self.CheckKeyword(keyword, cursor_1):
            
            #get all time in this keyword
            time_list = self.GetAllTimeline(cursor_1)
            
            #one day search
            if self.CheckOneDay(start_d, end_d):
                #no data in this time period
                if start_d not in time_list:
                    process_date = [start_d]

            #period day search
            else:
                #create a checkpoint
                checkpoint = self.SetContinuousCheckPoint(start_d, end_d)
                #contain the data that identify odd day / even day already
                process_date = self.CreateTimeline(start_d, end_d, checkpoint, time_list, checkpoint[2])
            return process_date
        
        #keyword doesn't exists
        else:
            print("Query does not exist in the collection.")
            return [None]

    #either continuous timeline or discrete timeline
    #create the date that need to be process
    def CreateTimelist(self, date_list, checkpoint, time_list, even):
        interval = 1
        time_delta = len(date_list)
        process_date = []
        cp1 = checkpoint[0]
        cp2 = checkpoint[1]

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
        
        print('date to sentiment(discrete)', process_date)
        return process_date
    
    #discrete timeline or continuous timeline
    #create the date that need to be process
    def CheckDBTimelist(self, keyword, date_list, collection_name):
        db_action  = self.db_action
        time_list = []
        process_date = []
        db_action.not_print_raw() #turn off status printing

        #select the collection
        collection = db_action.tweetdb_object(db_action.tweetdb_object(config.mongo_client, config.database_name, collection_name))
        query_object_1 = db_action.tweetdb_create_object(['keyword'],[keyword])
        cursor_1 = db_action.tweetdb_find(collection_name, collection, query_object_1)
        
        #keyword exists
        if self.CheckKeyword(keyword, cursor_1):
            #get all time in this keyword
            time_list = self.GetAllTimeline(cursor_1)

            #one day search
            if self.CheckOneDay(date_list[0], date_list[-1]):
                if date_list[0] not in time_list:
                    process_date = [date_list[0]]
            else:
                #create a checkpoint
                #return index of the date
                checkpoint = self.SetDiscreteCheckPoint(date_list)
                #contain the data that identify odd day / even day already
                process_date = self.CreateTimelist(date_list, checkpoint, time_list, checkpoint[2])
            return process_date
        #keyword doesn't exists
        else:
            print('Query does not exist in the collection')
            return [None]

    #can only extract 7 days ago period
    def Extract(self, keyword):

        #connect to tweepy
        api = self.ConnectTweepy()

        #search by keyword
        tweepy_search.PullTwitterData().search_twitter(api, keyword, self.search_type, self.search_limit)

    #transform by keyword (# or word)
    #transform by time

    #sentiment by keyword (# or word)
    def SentimentByKeyword(self, keyword):

        CheckSentiment = False
        CheckTransform = False
        CheckExtract = False

        #check if sentiment this keyword
        #check the timeline type
        #check if transformed this keyword
        #check if extract this keyword

    #sentiment by time
    def SentimentByTime(self, keyword, start_d, end_d):
        temp_date = []

        #check sentiment database
        sentiment_date = self.CheckDBTimeline(keyword, start_d, end_d, config.collection_name_5)

        while True:
            if sentiment_date==[]:
                print('show data visualization')
                break
            #data need to be sentiment before use
            else:
                sentiment_date = sorted(sentiment_date)
                check_con = self.CheckConsecutive(sentiment_date)

                #check if the specific date in cleaned database
                #continuous timeline
                if check_con:
                    cleaned_date = self.CheckDBTimeline(keyword, sentiment_date[0], sentiment_date[-1], config.collection_name_2)
                #discrete timeline
                else:
                    cleaned_date = self.CheckDBTimelist(keyword, sentiment_date, config.collection_name_2)
                
                #if that date don't have cleaned data then transform
                if cleaned_date != []:
                    #transform until every data of the specific date can't be transform
                    print('transform')
                #if have that date in cleaned data then sentiment
                else:
                    #sentiment until every data of the specific date can't be sentiment
                    print('sentiment')
                
                #will be in transform function
                #find the date that hasn't sentiment
                for date in sentiment_date:
                    if date not in cleaned_date:
                        #insert the date that hasn't sentiment
                        temp_date.append(date)

                #check if every date has been sentiment
                #if not then extract
                if temp_date != []:
                    print('extract')
                else:
                    print('finish the task')

        #check if sentiment this keyword on this period
        #check timeline type
        #check if transformed this keyword on this period
        #check if extract this keyword on this period

if __name__ == '__main__':
    mainoperation = MainOperation()

    start_date = datetime.date(2022, 12, 30) #y m d
    # end_date = datetime.date(2023, 1, 15)
    end_date = datetime.date(2023, 1, 16)

    # mainoperation.CheckDB('#มั่วๆ', [], config.collection_name_5)