import config
import database_action
import collections

db_action = database_action.DatabaseAction()

class Ranking():
    
    def pull_word(self):
        cursor = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
        
        data_field = ["_id"]
        data_list = [0]
        
        db_action.not_print_raw()

        query_object = db_action.tweetdb_create_object(data_field, data_list)
        show_cursor = db_action.tweetdb_show_collection(config.collection_name_2, cursor, query_object)

        return show_cursor
    
    def rank_word(self):
        cursor = self.pull_word()
        db_action.not_print_raw()
        
        total_list = []

        for doc in cursor:
            total_list += list(doc.values())[0]

        rank_dict = dict(collections.Counter(total_list))

        rank_dict = dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))

        ranking_key = list(rank_dict.keys())

        ranking_frequency = list(rank_dict.values())

        test_set = list(enumerate(sorted(set(ranking_frequency), reverse=True), start=1))

        top_dict = []

        for i in range(config.ranking_top):
            temp = ''
            for j in range(len(ranking_key)):
                
                if test_set[i][1] == ranking_frequency[j]:
                    temp += ' ' + ranking_key[j] + ' (%s)'%str(ranking_frequency[j])
            print('[%d] %s'%(test_set[i][0], temp))
            
if __name__ == '__main__':
    Ranking().rank_word()