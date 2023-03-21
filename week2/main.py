import Extract
import Sentiment
import Transform
import config
import datetime
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
        
    def IsValidDate(self, start_d, end_d):
        today = datetime.date.today()
        interval = datetime.timedelta(days=1)
        time_delta = end_d-start_d
        check_date = start_d

        for i in range(time_delta.days+1):
            if check_date.day > today.day:
                return False
            check_date+=interval
        return True
    
    def IsLast7Days(self, start_d, end_d):
        last7days = datetime.date.today() - datetime.timedelta(days=7)
        interval = datetime.timedelta(days=1)
        time_delta = end_d-start_d
        check_date = start_d

        for i in range(time_delta.days+1):
            if check_date.day < last7days.day:
                return False
            check_date+=interval
        return True
    
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
    
    #always continuous timeline
    #create the date that need to be process
    def CreateTimeline(self, start_d, end_d, checkpoint, time_list, even):
        interval = datetime.timedelta(days=1)
        process_date = []
        cp1 = checkpoint[0]
        cp2 = checkpoint[1]
        date_list = []
        
        print(start_d, end_d)

        #odd number
        if not even:
            cp = checkpoint[0]+interval
            date_list.append(cp)
            #check the first checkpoint
            if cp not in time_list :
                process_date.append(cp)
            
        while True:
            #cp1 meet the start point, cp2 meet the end point
            if cp1 == start_d-interval or cp2 == end_d+interval:
                break
            date_list.append(cp1)
            date_list.append(cp2)
            #check checkpoint 1
            if cp1 not in time_list:
                process_date.append(cp1)
            cp1 -= interval
            #check checkpoint 2
            if cp2 not in time_list:
                process_date.append(cp2)
            cp2+=interval

        return process_date

    #sentiment by keyword
    def Perform(self, keyword, settings):

        #cleaned database
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        query_object = db_action.tweetdb_create_object(['keyword'],[keyword])

        #sentiment by time
        if settings['mode'] == 'time':
            start_d = settings['start_d']
            end_d = settings['end_d']
            
            #check if the date valid
            #if invalid date
            if not self.IsValidDate(start_d, end_d):
                return 'Invalid Timeline'
            
            #if valid date then check if keyword exists
            #if keyword not exist
            if not self.IsMatch(collection, query_object):
                print('keyword not exist')
                #check if the date in last 7 days
                #if the date not in last 7 days period then return no data
                if not self.IsLast7Days(start_d, end_d):
                    return 'No data in this period'
                #if the date is in last 7 days period
                #extract
                process_id = self.Extract(keyword, settings)
                #transform
                tf = self.TransformByKeyword(keyword, process_id, by_id=True)

                #sentiment
                sentiment = Sentiment.SentimentAnalysis()
                sentiment_dict = sentiment.Perform(keyword)
                if sentiment_dict == None:
                    return 'No data in this period'
                return sentiment_dict
            #if keyword exist then check if have all data for every period
            #pull all date in cleaned database
            cursor = db_action.tweetdb_find(config.collection_name_2, collection, query_object)
            time_list = self.GetAllTimeline(cursor)
            
            #one day search
            #if it is one day search
            if self.CheckOneDay(start_d, end_d):
                
                # this date is exist in cleaned database
                if start_d in time_list:
                    print('keyword exist + one day + date exist')
                    #sentiment
                    sentiment = Sentiment.SentimentAnalysis()
                    sentiment_dict = sentiment.Perform(keyword)
                    if sentiment_dict == None:
                        return 'No data in this period'
                    return sentiment_dict
                print('keyword exist + one day + date not exist')
                #this date is not exist in cleaned database
                #check if the date in last 7 days
                #if the date not in last 7 days period then return no data
                if not self.IsLast7Days(start_d, end_d):
                    return 'No data in this period'
                #if the date is in last 7 days period
                #extract
                process_id = self.Extract(keyword, settings)
                #transform
                tf = self.TransformByKeyword(keyword, process_id, by_id=True)

                #sentiment
                sentiment = Sentiment.SentimentAnalysis()
                sentiment_dict = sentiment.Perform(keyword)
                if sentiment_dict == None:
                    return 'No data in this period'
                return sentiment_dict
            #period day search
            else:
                #create a checkpoint
                checkpoint = self.SetContinuousCheckPoint(start_d, end_d)
                #contain the data that identify odd day / even day already
                check_id = self.CreateTimeline(start_d, end_d, checkpoint, time_list, checkpoint[2])

                #still have data that not been sentiment yet
                if check_id != []:
                    #check if the date in last 7 days
                    #if the date not in last 7 days period then return no data
                    if not self.IsLast7Days(start_d, end_d):
                        return 'No data in this period'
                    #if the date is in last 7 days period
                    #extract
                    process_id = self.Extract(keyword, settings)
                    #transform
                    tf = self.TransformByKeyword(keyword, process_id, by_id=True)
                    
                    #sentiment
                    sentiment = Sentiment.SentimentAnalysis()
                    sentiment_dict = sentiment.Perform(keyword)
                    if sentiment_dict == None:
                        return 'No data in this period'
                    return sentiment_dict
                #all data is in cleaned database
                #sentiment
                sentiment = Sentiment.SentimentAnalysis()
                sentiment_dict = sentiment.Perform(keyword)
                if sentiment_dict == None:
                    return 'No data in this period'
                return sentiment_dict
            
        #sentiment by keyword
        elif settings['mode'] == 'keyword':

            #check if keyword exists in cleaned database
            #if keyword not match then extract
            if not self.IsMatch(collection, query_object):
                #extract
                process_id = self.Extract(keyword, settings)

                #transform
                tf = self.TransformByKeyword(keyword, process_id, by_id=True)

                #sentiment
                sentiment = Sentiment.SentimentAnalysis()
                sentiment_dict = sentiment.Perform(keyword)
                if sentiment_dict == None:
                    return 'No data in this period'
                return sentiment_dict 
            #if keyword match then sentiment
            sentiment = Sentiment.SentimentAnalysis()
            sentiment_dict = sentiment.Perform(keyword)
            if sentiment_dict == None:
                return 'No data in this period'
            return sentiment_dict                
        else:
            return 'Invalid perform mode'
        
if __name__ == '__main__':
    mainoperation = MainOperation()
    # settings for sentiment by keyword
    settings = {
        'search_type' : config.search_type,
        'num_tweet' : config.num_tweet,
        'start_d' : datetime.date(2023, 3, 15),
        'end_d': datetime.date(2023, 3, 20),
        'mode' : 'keyword'
    }

    #settings for sentiment by time
    # settings = {
    #     'search_type' : config.search_type,
    #     'num_tweet' : config.num_tweet,
    #     'start_d' : datetime.date(2023, 3, 20),
    #     'end_d': datetime.date(2023, 3, 21),
    #     'mode' : 'time'
    # }
    keyword = config.search_word

    sentiment_dict = mainoperation.Perform(keyword, settings)
    print(sentiment_dict)
