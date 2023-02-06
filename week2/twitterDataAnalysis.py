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
    
    def pull_sentiment(self):
        cursor = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_5)

        data_field = ["_id", "input", "polarity"]
        data_list = [0,1,1]

        db_action.not_print_raw()

        query_object = db_action.tweetdb_create_object(data_field, data_list)
        show_cursor = db_action.tweetdb_show_collection(config.collection_name_5, cursor, query_object)
        return show_cursor

    def sentiment_cal(self, rank_dict):
        cursor = self.pull_sentiment()

        top_words = list(rank_dict.values())
        rank_index = list(rank_dict.keys())
        
        input_list_text = []
        input_list_polar = []
        polarity = []

        for doc in cursor:
            input_list_text.append(doc['input'])
            input_list_polar.append(doc['polarity']) 

        # test = 'hbo go หนัง ซีรีส์ ทั่วโลก โหลด ดู ออฟ ไลน์ สอบถาม สั่งซื้อ dm line lhrzg หาร hbogo hbogo หาร hbogo ราคาถูก หาร hbo ราคาถูก รีวิว หนัง hbogo หาร hbogo ราคาถูก หาร hbogo hbogo'
        # print('หนัง ' in test)

        # print(top_words)
        print('{:<5}'.format('rank'),'{:<10}'.format('word'), '{:<10}'.format('sentiment'))


        for i in range(len(top_words)):
            polarity = []
            for j in range(len(input_list_text)):
                if top_words[i] in input_list_text[j]:
                    polarity.append(input_list_polar[j])

            if sum(polarity) > 0:
                sentiment = '+'
            elif sum(polarity) < 0:
                sentiment = '-'
            elif sum(polarity) == 0:
                sentiment = 'N'
            
<<<<<<< Updated upstream
            print(word ,sum(polarity), len(polarity))
            # print(word, polarity)
            # print(word, input_list_polar[i], len(polarity))
            
=======
            print('{:<5}'.format(rank_index[i]),'{:<10}'.format(top_words[i]) , '{:<10}'.format(sentiment))
    
>>>>>>> Stashed changes
    def rank_word(self, rank_set, rank_key, rank_f):

        top_dict = {}

        for i in range(config.ranking_top):
            temp = ''
            temp2 = ''
            for j in range(len(rank_key)):
                
                if rank_set[i][1] == rank_f[j]:
                    temp += ' ' + rank_key[j] + ' (%s)'%str(rank_f[j])
                    temp2 += ' ' + rank_key[j]
            
            top_dict[rank_set[i][0]] = temp2
        return top_dict
        
    def rank_list(self):
        
        cursor = self.pull_word()
        db_action.not_print_raw()

        total_list = []

        for doc in cursor:
            total_list += list(doc.values())[0]

        rank_dict = dict(collections.Counter(total_list))
        rank_dict = dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))

        ranking_key = list(rank_dict.keys())
        ranking_frequency = list(rank_dict.values())

        rank_set = list(enumerate(sorted(set(ranking_frequency), reverse=True), start=1))

        self.sentiment_cal(self.rank_word( rank_set, ranking_key, ranking_frequency))
        
        query_object = db_action.tweetdb_create_object(ranking_key,ranking_frequency )
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_6)
        
        # insert to db 
        db_action.tweetdb_insert(config.collection_name_6, collection, query_object)
            
if __name__ == '__main__':
    Ranking().rank_list()