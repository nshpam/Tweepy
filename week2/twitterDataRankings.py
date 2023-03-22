import config
import database_action
import collections
import cProfile

db_action = database_action.DatabaseAction()
#turn off printing database status
db_action.not_print_raw() 

class Ranking():
    
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
    
    # def pull_sentiment(self):
    #     cursor = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)

    #     data_field = ["_id", "input", "polarity"]
    #     data_list = [0,1,1]

    #     db_action.not_print_raw()

    #     query_object = db_action.tweetdb_create_object(data_field, data_list)
    #     show_cursor = db_action.tweetdb_show_collection(config.collection_name_5, cursor, query_object)
    #     return show_cursor

    # def sentiment_cal(self, rank_dict):
    #     cursor = self.pull_sentiment()

    #     top_words = list(rank_dict.values())

    #     rank_index = list(rank_dict.keys())
        
    #     input_list_text = []
    #     input_list_polar = []
    #     polarity = []

    #     for doc in cursor:
    #         input_list_text.append(doc['input'])
    #         input_list_polar.append(doc['polarity']) 

    #     print('{:<5}'.format('rank'),'{:<10}'.format('word'), '{:<10}'.format('sentiment'))

    #     for i in range(len(top_words)):
    #         polarity = []
    #         for j in range(len(input_list_text)):
    #             if top_words[i] in input_list_text[j]:
    #                 polarity.append(input_list_polar[j])

    #         if sum(polarity) > 0:
    #             sentiment = '+'
    #         elif sum(polarity) < 0:
    #             sentiment = '-'
    #         elif sum(polarity) == 0:
    #             sentiment = 'N'
            
    #         print('{:<5}'.format(rank_index[i]),'{:<10}'.format(top_words[i]) , '{:<10}'.format(sentiment))
    
    def rank_word(self, rank_set, rank_key, rank_f):

        top_word = []
        top_f = []

        top_dict = {}

        for i in range(config.ranking_top):
            temp = ''
            temp2 = ''
            for j in range(len(rank_key)):
                
                if rank_set[i][1] == rank_f[j]:
                    temp += rank_key[j] 
                    temp2 += str(rank_f[j])
                    break
            
            top_dict[rank_set[i][0]] = [temp, temp2]

            top_word.append(temp)
            top_f.append(temp2)
        return top_dict
        
    def rank_list(self, keyword):

        #pull word from tokenization database
        cursor = self.PullCleaned(keyword)
        #turn off printing raw
        db_action.not_print_raw()

        total_list = []

        #append all the word from every tweet into total_list
        for doc in cursor:
            total_list+= list(doc['text'])
        
        #counting the frequency of elements
        rank_dict = dict(collections.Counter(total_list))
        #sort from high to low
        rank_dict = dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))
        #create a list from word
        ranking_key = list(rank_dict.keys())
        #create a list from word frequency
        ranking_frequency = list(rank_dict.values())
        #ranking by frequency
        # rank_set = list(enumerate(sorted(set(ranking_frequency), reverse=True), start=1))

        #ranking by key
        # print(self.rank_word(rank_set, ranking_key, ranking_frequency))
        # return the top words and their frequencies
        return ranking_key[:config.ranking_top], ranking_frequency[:config.ranking_top]

        #ranking by hashtags

        #ranking by frequency but showing its sentiments
        # self.sentiment_cal(self.rank_word( rank_set, ranking_key, ranking_frequency))
            
if __name__ == '__main__':

    # cProfile.run('Ranking().rank_list()')
    # Ranking().rank_list()
    top_words, top_frequencies = Ranking().rank_list(config.search_word)

    print(top_words, top_frequencies)
