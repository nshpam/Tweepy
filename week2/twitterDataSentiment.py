import config
import database_action
import requests
import time
#for testing
import datetime

#initialize database action function
db_action = database_action.DatabaseAction()

#Sentiment analysis function
class SentimentAnalysis():
    
    #Check if have the keyword in database
    def IsMatch(self, collection, query_object):
        #no keyword match
        if collection.count_documents(query_object) == 0:
            return False
        #keyword match
        return True

    #pull clean data from cleaned database
    def PullCleanByKeyword(self, keyword):
        db_action.not_print_raw() #turn off printing database status

        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        #create query object
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        #query
        cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)
        
        #check if have the keyword
        if not self.IsMatch(collection, query_object):
            return None
        return cursor
    
    #the date_list is the date that need to be sentiment which not sentiment yet
    def PullCleanByTime(self, keyword, date_list):
        sentiment_dict = {} #storing the data that can perform sentiment
        transform_list = [] #storing the date that can't perform sentiment
        data_dict = {} #storing the data for sentimental and transformation
        check_transform = [] #temperary storing date

        db_action.not_print_raw() #turn off printing database status

        #connect with cleaned database
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        query_object = db_action.tweetdb_create_object(['keyword'],[keyword])
        cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)
        
        #check if have the keyword
        if not self.IsMatch(collection, query_object):
            return None

        #pull all time from database
        for doc in cursor:
            for date in date_list:
                if doc['date'].date() == date:
                    sentiment_dict[doc['id']] = [doc['keyword'], doc['date'].date(), doc['text']]
                    check_transform.append(date)

        #check which date should be extract
        for date in date_list:
            if date not in check_transform:
                transform_list.append(date)
        
        #collect sentiment data and date to extract
        data_dict['sentiment'] = sentiment_dict
        data_dict['transform'] = transform_list

        return data_dict
    
    #analyze which intention the data is
    def intention_analysis(self, intention):
        
        #collect intention
        intention_type = list(intention.keys())
        #collection intention value
        intention = list(intention.values())
        conclusion = {}
        
        #create the conclusion base-on intention
        for i in range(len(intention_type)):
            if intention[i] != '0':
                conclusion[intention_type[i]] = intention[i]
        
        return conclusion
    
    #convert_polarity of the data
    def convert_polarity(self, polar):

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
    def SentimentByKeyword(self, cursor, id_list):
        sentiment_dict = {}

        #iterate all data in cursor
        for doc in cursor:
            if doc['id'] not in id_list:
                continue
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
                polar = self.convert_polarity(raw['sentiment']['polarity'])
                #intention analysis
                conclusion = self.intention_analysis(raw['intention'])
                #collect data for insertion
                sentiment_dict[doc['id']] = [doc['id'], doc['keyword'], doc['date'], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
            
            except:
                #collect data for insertion
                sentiment_dict[doc['id']] = ['error']
                
                #print the error on console
                print('sentiment error')
                print(doc['id'],doc['keyword'], doc['date'], ' '.join(doc['text']))
            #delay for SSense API
            time.sleep(0.5)
        return sentiment_dict

    #sentiment by date
    def SentimentByTime(self, sentiment_raw):
        
        sentiment_dict = {}

        #seperating id and data
        sentiment_key = list(sentiment_raw.keys())
        sentiment_data = list(sentiment_raw.values())

        #iterate data in sentiment data
        for i in range(len(sentiment_data)):
            #sentiment with SSense
            res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(sentiment_data[i][2])})

            #catch the response from SSense
            try:
                #convert SSense reponse into Json format
                raw = res.json()

                #return alert from sentiment
                if raw['alert'] != []:
                    print('ALERT:',raw['alert'])
                    sentiment_dict[sentiment_key[i]] = [raw['alert']]
                    continue

                #converting polar for calculation
                polar = self.convert_polarity(raw['sentiment']['polarity'])
                #intention analysis
                conclusion = self.intention_analysis(raw['intention'])
                #collect data for insertion
                sentiment_dict[sentiment_key[i]] = [sentiment_key[i] ,sentiment_data[i][0], sentiment_data[i][1], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
            except:
                #collect data for insertion
                sentiment_dict[sentiment_key[i]] = ['error']
                print('sentiment error :', sentiment_key[i], sentiment_data[i][0], sentiment_data[i][1])
            #delay for SSense API
            time.sleep(0.5)
        return sentiment_dict
    
    #perform the sentiment base-on sentiment_type
    def Perform(self, keyword, date_list, sentiment_type, id_list=[]):
        sentiment_dict = {}

        #sentiment by time
        if sentiment_type == 'time':
            #create data list for sentiment 
            data_dict = self.PullCleanByTime(keyword, date_list)

            #no keyword match
            if data_dict == None:
                sentiment_dict['sentiment'] = []
                sentiment_dict['transform'] = date_list
                return sentiment_dict
            
            #perform the sentiment by time
            sentiment_dict['sentiment'] = self.SentimentByTime(data_dict['sentiment'])
            sentiment_dict['transform'] = data_dict['transform']
            
        #sentiment by keyword
        elif sentiment_type == 'keyword':
            #create cursor for sentimenting by keyword
            #which cursor has been filter by keyword already 
            cursor = self.PullCleanByKeyword(keyword)
            
            #no keyword match
            if cursor == None:
                sentiment_dict['sentiment'] = []
                sentiment_dict['transform'] = [keyword]
                return sentiment_dict
            #perform the sentiment by keyword and return sentiment dict
            sentiment_dict['sentiment'] = self.SentimentByKeyword(cursor, id_list)
            sentiment_dict['transform'] = []
                
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
    # print('extract :', sentiment_dict['extract'])
    
    
    #test from tweepy_main.py
    #some sentiment and the one that not sentiment have in cleaned database
    #some sentiment and the one that not sentiment don't have in cleaned database
    #some sentiment and the one that not sentiment some have in cleaned database

    

    