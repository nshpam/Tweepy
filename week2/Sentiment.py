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
        query_object = db_action.tweetdb_create_object(['keyword'],[keyword])
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
    
    #sentiment by keyword
    def Perform(self, keyword):
        sentiment_dict = {}
        cursor = self.PullCleaned(keyword)

        #keyword not match
        if cursor == None:
            return None

        #iterate all data in cursor
        for doc in cursor:
            #perform a sentiment
            res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(doc['text'])})
            #catch the response from SSense
            try:
                #convert SSense response into Json format
                raw = res.json()
                
                #return alert from sentiment
                if raw['alert'] != []:
                    print('ALERT:',raw['alert'])
                    #collect data for insertion
                    sentiment_dict[doc['id']] = [raw['alert']]
                    continue
                    
                #converting polar for calculation
                polar = self.ConvertPolar(raw['sentiment']['polarity'])
                #collect data for insertion
                sentiment_dict[doc['id']] = {'id' : doc['id'], 'keyword' : doc['keyword'], 'date' : doc['date'], 'input' : raw['preprocess']['input'], 'score': raw['sentiment']['score'], 'polar':polar}
            except:
                #collect data for insertion
                sentiment_dict[doc['id']] = {'err':'error'}
                
                #print the error on console
                print('sentiment error')
                print(doc['id'],doc['keyword'], doc['date'], ' '.join(doc['text']))
            #delay for SSense API
            time.sleep(0.5)
        return sentiment_dict


        