import config
import database_action
import requests
import time

db_action = database_action.DatabaseAction()

class SentimentAnalysis():

    def __init__(self, count_db=0):
        self.count_db = count_db

    #pull clean data from database
    def PullCleanByKeyword(self, keyword):
        db_action.not_print_raw()
        cursor = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        show_cursor = db_action.tweetdb_find(config.collection_name_2, cursor, query_object)

        return show_cursor
    
    def PullCleanByTime(self, keyword, date_list):
        cleaned_list = []
        db_action.not_print_raw()
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        
        for date in date_list:
            query_object = db_action.tweetdb_create_object(['keyword', 'date'],[keyword, date])
            show_cursor = db_action.tweetdb_find(config.collection_name_2, cursor, query_object)
    
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

    def SentimentByTime(self, keyword, cursor, date_list):

        sentiment_dict = {}

        for doc in cursor:
            pass

        for doc in cursor:
            if doc['keyword'] == keyword:
                for date in date_list:
                    if doc['date'].date() == date:

                        #sentiment
                        res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(doc['text'])})
                        try:
                            raw = res.json()

                            if raw['alert'] != []:
                                print('ALERT! :',raw['alert'])

                            #converting polar for calculation
                            polar = self.convert_polarity(raw['sentiment']['polarity'])
                            #intension analysis
                            conclusion = self.intention_analysis(raw['intention'])

                            sentiment_dict[doc['id']] = [doc['keyword'], doc['date'], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]

                            # data_field = ['id', 'keyword', 'date', 'text', 'score', 'polarity', 'intention']
                            # data_list = [doc['id'], doc['keyword'], doc['date'], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
                            # query_object = db_action.tweetdb_create_object(data_field, data_list)

                            # collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)
                            # #insert to db
                            # db_action.tweetdb_insert(config.collection_name_5, collection, query_object)

                        except:
                            print('sentiment error')
                            return []
            time.sleep(0.5)
        return sentiment_dict

    def SentimentByKeyword(self, keyword, cursor):
        sentiment_dict = {}
        for doc in cursor:
            if doc['keyword'] == keyword:
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
                    return []
            time.sleep(0.5)
        return sentiment_dict
    
    def Perform(self, keyword, date_list, sentiment_type):

        #start the timer
        tic = time.perf_counter()
        self.count_db = 0
        
        
        #sentiment by time
        if sentiment_type == 'time':
            cursor = self.PullCleanByTime(keyword, date_list)
            sentiment_data = self.SentimentByTime(keyword, cursor, date_list)
            if sentiment_data != []:
                #insert data
                return True
            #Failed to sentiment
            return False
        #sentiment by keyword
        elif sentiment_type == 'keyword':
            sentiment_data = self.SentimentByKeyword(keyword, cursor, )
        #invalid sentiment type
        else:
            return False

        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        print('TOTAL TOKENIZATION :', self.count_token + self.count_untoken)
                

if __name__ == '__main__':
    SentimentAnalysis().Sentiment()

    print('finish insertion')