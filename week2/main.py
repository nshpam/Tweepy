import Extract
import Sentiment
import Transform
import config
import datetime
import tweepy
import database_action
import numpy as np

db_action = database_action.DatabaseAction()
db_action.not_print_raw()

class MainOperation():

    def CheckConsecutive(self, date_list):
        #return True if differences between consecutive numbers
        #which means it's a continuous timeline
        if np.all(np.diff(sorted(date_list))==1):
            return True
        return False

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

    #check if it's a timeline or a day
    def CheckOneDay(self, start_d, end_d):
        if start_d == end_d:
            return True
        return False
    
    #update extract data
    def UpdateExtract(self, id, fav_count, retweet_count):
        data_field = ['favorite_count', 'retweet_count']
        data_list = [fav_count, retweet_count]
        query_object = db_action.tweetdb_create_object(data_field,data_list)
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

        db_action.tweetdb_update(config.collection_name, collection, query_object, 'id', id)
    
    def RemoveTweetsURL(self, cursor):
        all_data = []
        filters = Transform.FilterData()

        for doc in cursor:
            raw_list = doc['text'].split()
            clean_data = ''
            for word in raw_list:
                if not filters.FilterUrl(word):
                    clean_data+=word
            all_data.append(clean_data)
        
        return all_data

    def IsContext(self, text):
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)
        query_object = db_action.tweetdb_create_object(["text"],[1])
        cursor = db_action.tweetdb_show_collection(config.collection_name, collection, query_object)

        raw_list = text.split()
        clean_data = ''
        filters = Transform.FilterData()

        for word in raw_list:
            if not filters.FilterUrl(word):
                clean_data += word
        
        if clean_data in self.RemoveTweetsURL(cursor):
            return True
        return False

    def Extract(self, keyword, settings):
        extract = Extract.ExtractTwitter()
        #search the twitter
        tweet_list = extract.SearchTwitter(keyword, settings)
        #extract twitter
        tweet_dict = extract.Perform(keyword, tweet_list)
        #all extract id
        extract_id = list(tweet_dict.keys())
        #filtered extract id
        return_id = []

        #check if have data of this keyword
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)
        data_field = ['id', 'keyword', 'username', 'date', 'location', 'text', 'favorite_count', 'retweet_count']

        for id in extract_id:
            query_object_2 = db_action.tweetdb_create_object(["keyword","id"], [keyword,id])
            
            #if duplicate id then update
            if self.IsMatch(collection, query_object_2):
                self.UpdateExtract(id, tweet_dict[id]['favorite_count'], tweet_dict[id]['retweet_count'])

            #if not duplicate context then insert data 
            elif not self.IsContext(tweet_dict[id]['text']):
                data_list = [id, keyword, tweet_dict[id]['username'], tweet_dict[id]['date'], tweet_dict[id]['location'], tweet_dict[id]['text'], tweet_dict[id]['favorite_count'], tweet_dict[id]['retweet_count']]
                query_object_3 = db_action.tweetdb_create_object(data_field, data_list)
                #insert data
                db_action.tweetdb_insert(config.collection_name, collection, query_object_3)
                return_id.append(id)

        return return_id

    def TransformByKeyword(self, keyword, id_list, by_id):
        #tokenize
        tokenization = Transform.Tokenization()
        tokened_dict = tokenization.Perform(keyword, id_list, by_id)
        # print('tokened_id: ',tokened_dict)

        if tokened_dict == {}:
            return False

        #normalize
        normalize = Transform.Normalize()
        normalized_dict = normalize.Perform(list(tokened_dict.values()))
        # print('normalized_dict: ',normalized_dict)

        #cleaning
        clean = Transform.CleanThaiAndEng()
        cleaned_dict = clean.Perform(list(normalized_dict.values()))
        # print('cleaned_dict: ', cleaned_dict)

        transformed_list = list(cleaned_dict.values())

        #insert data to cleaned database
        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)

        #create data object
        data_field = ['id', 'keyword', 'date', 'text']
        for data in transformed_list:
            data_list = [data['id'], data['keyword'], datetime.datetime.combine(data['date'], datetime.time.min), data['text']]
            query_object = db_action.tweetdb_create_object(data_field, data_list)

            #check duplicate data before insertion
            check_query = db_action.tweetdb_create_object(["id"],[data['id']])

            if not self.IsMatch(collection, check_query):
                db_action.tweetdb_insert(config.collection_name_2, collection, query_object)

        return True
        


    #sentiment by keyword
    def Perform(self, keyword, settings):

        #sentiment by time
        if settings['mode'] == 'time':
            pass
        #sentiment by keyword
        elif settings['mode'] == 'keyword':
            #cleaned database
            collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
            query_object = db_action.tweetdb_create_object(['keyword'],[keyword])
            
            #check if keyword exists in cleaned database
            #if keyword not match then extract
            if not self.IsMatch(collection, query_object):
                #extract transform sentiment return data
                #extract
                process_id = self.Extract(keyword, settings)
                # print('process_id:',process_id)

                #transform
                tf = self.TransformByKeyword(keyword, process_id, by_id=True)

                if tf:
                    #sentiment
                    sentiment = Sentiment.SentimentAnalysis()
                    sentiment_dict = sentiment.Perform(keyword)
                    return sentiment_dict
            #if keyword match then sentiment
            sentiment = Sentiment.SentimentAnalysis()
            sentiment_dict = sentiment.Perform(keyword)
            if sentiment_dict == None:
                return 'No data in this period'
            return sentiment_dict

                
            #if keyword match then transform
        else:
            return 'Invalid perform mode'
        
if __name__ == '__main__':
    mainoperation = MainOperation()
    settings = {
        'search_type' : config.search_type,
        'num_tweet' : config.num_tweet,
        'start_d' : datetime.date(2023, 3, 17),
        'end_d': datetime.date(2023, 3, 20),
        'mode' : 'keyword'
    }
    keyword = config.search_word
    sentiment_dict = mainoperation.Perform(keyword, settings)
    print(sentiment_dict)
