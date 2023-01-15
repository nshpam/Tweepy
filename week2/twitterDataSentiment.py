import config
import database_action
import requests
import time

db_action = database_action.DatabaseAction()

class SentimentAnalysis():

    def pull_clean(self):
        cursor = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        
        data_field = ["_id"]
        data_list = [0]
        
        query_object = db_action.tweetdb_create_object(data_field, data_list)
        show_cursor = db_action.tweetdb_show_collection(config.collection_name_2, cursor, query_object)

        return show_cursor
    
    def intention_analysis(self, intention):

        intention_type = list(intention.keys())
        intension_int = list(intention.values())
        conclusion = {}
        
        for i in range(len(intention_type)):
            if intension_int[i] != '0':
                conclusion[intention_type[i]] = intension_int[i]
        
        return conclusion
    
    def convert_polarity(self, polar):

        converted_polar = 0

        if polar == 'positive':
            converted_polar = 1
        elif polar == 'negative':
            converted_polar = 0
        elif polar == '':
            converted_polar = 2
    
        return converted_polar

    def sentiment(self):
        cursor = self.pull_clean()
        db_action.not_print_raw()

        for doc in cursor:
            res = requests.get(config.SSense_URL, headers={'Apikey':config.LextoPlus_API_key}, params={'text':' '.join(list(doc.values())[0])})
            try:
                raw = res.json()

                if raw['alert'] != []:
                    print('ALERT! :',raw['alert'])

                polar = self.convert_polarity(raw['sentiment']['polarity'])
                conclusion = self.intention_analysis(raw['intention'])

                data_field = ['input','score', 'polarity', 'intention']
                data_list = [raw['preprocess']['input'] ,raw['sentiment']['score'], polar, conclusion]
                query_object = db_action.tweetdb_create_object(data_field, data_list)

                collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)
                #insert to db
                db_action.tweetdb_insert(config.collection_name_5, collection, query_object)
                # print(query_object)
                # break

            except:
                print('error')

            time.sleep(1)
                

if __name__ == '__main__':
    SentimentAnalysis().sentiment()

    print('finish insertion')