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
        cursor_dict = {}
        temp_list_1 = [] #storing the date that can perform sentiment
        temp_list_2 = [] #storing the date that can't perform sentiment
        #turn off printing database status
        db_action.not_print_raw()
        #connect with cleaned database
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        
        for date in date_list:
            query_object = db_action.tweetdb_create_object(['keyword', 'date'],[keyword, date])
            cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)
            if cursor.count() == 0:
                temp_list_2.append(cursor)
            else:
                temp_list_1.append(cursor)
        
        cursor_dict['sentiment'] = temp_list_1
        cursor_dict['transform'] = temp_list_2
        
        return cursor_dict
    
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

    def SentimentByTime(self, cursor_list):

        sentiment_dict = {}
        #cursor_list is filtered by keyword and date already
        for cursor in cursor_list:
            for doc in cursor:
                #sentiment
                res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(doc['text'])})
                try:
                    raw = res.json()

                    if raw['alert'] != []:
                        print('ALERT! :', raw['alert'])

                    #converting polar for calculation
                    polar = self.convert_polarity(raw['sentiment']['polarity'])
                    #intention analysis
                    conclusion = self.intention_analysis(raw['intention'])

                    sentiment_dict[doc['id']] = [doc['keyword'], doc['date'], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
                except:
                    sentiment_dict[doc['id']] = ['error']
                    print('sentiment error :', doc['keyword'], doc['date'])
                    # return sentiment_dict
                time.sleep(0.2)
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
            cursor_list = self.PullCleanByTime(keyword, date_list)
            #perform the sentiment by time and return the sentiment dict
            sentiment_dict['sentiment'] = self.SentimentByTime(cursor_list['sentiment'])
            sentiment_dict['transform'] = cursor_list['transform']
            
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

    date_list = [datetime.date(2022, 12, 30).day,
             datetime.date(2022, 12, 31).day,
             datetime.date(2023, 1, 11).day,
             datetime.date(2023, 1, 12).day,
             datetime.date(2023, 1, 13).day,
             datetime.date(2023, 1, 14).day,
             datetime.date(2023, 1, 15).day,
             datetime.date(2023, 1, 16).day,
             datetime.date(2023, 1, 17).day,
             datetime.date(2023, 1, 18).day]

    SentimentAnalysis().Perform(config.search_word, date_list, 'time')