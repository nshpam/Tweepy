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
        
    def rank_list(self, keyword):

        if type(keyword) != type('') or keyword == '':
            return 'Invalid Keyword'

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
        
        # return the top words and their frequencies
        return ranking_key[:config.ranking_top], ranking_frequency[:config.ranking_top]
            
if __name__ == '__main__':

    # cProfile.run('Ranking().rank_list()')
    # Ranking().rank_list()s
    top_words, top_frequencies = Ranking().rank_list(config.search_word)

    print(top_words, top_frequencies)
