import config
import database_action
import requests
import time
import datetime

db_action = database_action.DatabaseAction()

class SentimentAnalysis():

    def __init__(self, count_db=0):
        self.count_db = count_db

    #pull clean data from database
    def PullCleanByKeyword(self, keyword):
        #turn off printing database status
        db_action.not_print_raw()
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)
        #no keyword match
        if cursor.count() == 0:
            return None
        #keyword match
        return cursor
    
    #the date_list is the date that need to be sentiment which not sentiment yet
    def PullCleanByTime(self, keyword, date_list):
        sentiment_dict = {} #storing the date that can perform sentiment
        extract_list = [] #storing the date that can't perform sentiment
        data_dict = {}
        check_extract = []
        #turn off printing database status
        db_action.not_print_raw()
        #connect with cleaned database
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        query_object = db_action.tweetdb_create_object(['keyword'],[keyword])
        cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)
        
        #no keyword found
        if cursor.count() == 0:
            return None

        #pull all time from database
        for doc in cursor:
            for date in date_list:
                if doc['date'].date() == date:
                    sentiment_dict[doc['id']] = [doc['keyword'], doc['date'].date(), doc['text']]
                    check_extract.append(date)

        #check which date should be extract
        for date in date_list:
            if date not in check_extract:
                extract_list.append(date)
        
        #collect sentiment data
        data_dict['sentiment'] = sentiment_dict
        data_dict['extract'] = extract_list

        return data_dict
    
    #analyze which intension the data is.
    def intention_analysis(self, intention):

        intention_type = list(intention.keys())
        intension_int = list(intention.values())
        conclusion = {}
        
        for i in range(len(intention_type)):
            if intension_int[i] != '0':
                conclusion[intention_type[i]] = intension_int[i]
        
        return conclusion
    
    #convert_polarity of the data
    def convert_polarity(self, polar):

        converted_polar = 0

        if polar == 'positive':
            converted_polar = 1
        elif polar == 'negative':
            converted_polar = -1
        elif polar == '':
            converted_polar = 0
    
        return converted_polar

    def SentimentByTime(self, sentiment_dict):

        sentiment_key = list(sentiment_dict.keys())
        sentiment_data = list(sentiment_dict.values())

        #cursor_list is filtered by keyword and date already
        for i in range(len(sentiment_data)):
            #sentiment
            res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(sentiment_data[i][2])})

            try:
                raw = res.json()

                if raw['alert'] != []:
                    print('ALERT! :', raw['alert'])
                #converting polar for calculation
                polar = self.convert_polarity(raw['sentiment']['polarity'])
                #intention analysis
                conclusion = self.intention_analysis(raw['intention'])

                sentiment_dict[sentiment_key[i]] = [sentiment_data[i][0], sentiment_data[i][1], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
            except:
                sentiment_dict[sentiment_key[i]] = ['error']
                print('sentiment error :', sentiment_data[i][0], sentiment_data[i][1])
            time.sleep(0.1)
        return sentiment_dict

    def SentimentByKeyword(self, cursor):
        sentiment_dict = {}
        for doc in cursor:
           
            #sentiment
            res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(doc['text'])})
            try:
                raw = res.json()
                    
                if raw['alert'] != []:
                    print('ALERT :', raw['alert'])
                    
                #converting polar for calculation
                polar = self.convert_polarity(raw['sentiment']['polarity'])
                #intension analysis
                conclusion = self.intention_analysis(raw['intention'])

                sentiment_dict[doc['id']] = [doc['keyword'], doc['date'], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
            except:
                print('sentiment error')
                return {}
            time.sleep(0.2)
        return sentiment_dict
    
    def Perform(self, keyword, date_list, sentiment_type):

        self.count_db = 0
        sentiment_dict = {}
        #sentiment by time
        if sentiment_type == 'time':
            #create cursor list for sentimenting by time
            #which cursor list has been filter by keyword and date already 
            data_dict = self.PullCleanByTime(keyword, date_list)
            #perform the sentiment by time and return the sentiment dict
            sentiment_dict['sentiment'] = self.SentimentByTime(data_dict['sentiment'])
            sentiment_dict['extract'] = data_dict['extract']
            
        #sentiment by keyword
        elif sentiment_type == 'keyword':
            #create cursor for sentimenting by keyword
            #which cursor has been filter by keyword already 
            cursor = self.PullCleanByKeyword(keyword)
            #if keyword match
            if cursor != None:
                #perform the sentiment by keyword and return sentiment dict
                sentiment_dict = self.SentimentByKeyword(cursor)
            else:
                return None
        #invalid sentiment type
        else:
            return 'Invalid sentiment type'
        
        return sentiment_dict

if __name__ == '__main__':

    #all sentiment (date_list = [])
    #no such a case date_list will only be the date that need to be process only
    #which date_list already filter from tweepy_main.py already

    #all not sentiment but all have in cleaned database [FINISH]
    #all not sentiment but some have in cleaned database [FINISH]
    #all not sentiment but none have in cleaned database [FINISH]
    date_list = [datetime.datetime(2023, 1, 15).date(),
             datetime.datetime(2023, 1, 16).date(),
             datetime.datetime(2023, 1, 17).date(),
             datetime.datetime(2023, 1, 18).date()]

    sentiment_dict = SentimentAnalysis().Perform(config.search_word, date_list, 'time')
    print('sentiment :', sentiment_dict['sentiment'])
    print('extract :', sentiment_dict['extract'])
    
    
    #test from tweepy_main.py
    #some sentiment and the one that not sentiment have in cleaned database
    #some sentiment and the one that not sentiment don't have in cleaned database
    #some sentiment and the one that not sentiment some have in cleaned database

    

    