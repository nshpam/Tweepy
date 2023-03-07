import config
import database_action
import requests
import time

db_action = database_action.DatabaseAction()

class SentimentAnalysis():

    #pull clean data from database
    def PullClean(self, keyword):
        cursor = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        
        db_action.not_print_raw()
        
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        show_cursor = db_action.tweetdb_find(config.collection_name_2, cursor, query_object)

        return show_cursor
    
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
    
    def Sentiment(self, keyword):

        #start the timer
        tic = time.perf_counter()

        cursor = self.PullClean(keyword)

        #check the operation

        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        print('TOTAL TOKENIZATION :', self.count_token + self.count_untoken)

        for doc in cursor:
            res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(doc['text'])})
            try:
                raw = res.json()

                if raw['alert'] != []:
                    print('ALERT! :',raw['alert'])

                polar = self.convert_polarity(raw['sentiment']['polarity'])
                conclusion = self.intention_analysis(raw['intention'])

                #use the score to calculate overall sentiment
                data_field = ['id', 'keyword', 'date', 'text', 'score', 'polarity', 'intention']
                data_list = [doc['id'], doc['keyword'], doc['date'], raw['preprocess']['input'], raw['sentiment']['score'], polar, conclusion]
                query_object = db_action.tweetdb_create_object(data_field, data_list)

                collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)
                #insert to db
                db_action.tweetdb_insert(config.collection_name_5, collection, query_object)

            except:
                print('error')

            time.sleep(0.5)
                

if __name__ == '__main__':
    SentimentAnalysis().Sentiment()

    print('finish insertion')