import config
import database_action
import requests
import time
#for testing
import datetime

#initialize database action function
db_action = database_action.DatabaseAction()
#turn off printing database status
db_action.not_print_raw() 

#sentiment analysis function
class SentimentAnalysis():

    #check id have the keyword in database
    def IsMatch(self, collection, query_object):
        #no keyword match
        if collection.count_documents(query_object) == 0:
            return False
        #keyword match
        return True
    
    #pull data from cleaned database
    def PullCleaned(self, keyword):
        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        #create query object
        query_object = db_action.tweetdb_create_object(['keyword'],keyword)
        cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)

        #check if have the keyword
        if not self.IsMatch(collection, query_object):
            return None
        return cursor
    
    #convert polarity of the data
    def ConvertPolar(self, polar):
        converted_polar = 0

        #converting polarity into integers
        if polar == 'positive':
            converted_polar = 1
        elif polar == 'negative':
            converted_polar = -1
        elif polar == '':
            converted_polar = 0
        
        return converted_polar
        
        