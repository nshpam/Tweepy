import config
import database_action
import collections
import cProfile

db_action = database_action.DatabaseAction()

class Ranking():

    def __init__(self, activate_f=True, activate_s=True, activate_w=True):
        self.activate_f = activate_f
        self.activate_s = activate_s

    def show_frequency(self):
        self.activate_f = True
        return self.activate_f
    
    def hid_frequency(self):
        self.activate_f = False
        return self.activate_f

    def show_sentiment(self):
        self.activate_s = True
        return self.activate_s
    
    def hid_sentiment(self):
        self.activate_s = False
        return self.activate_s
    
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

        print(top_words)

        return

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
            
            print('{:<5}'.format(rank_index[i]),'{:<10}'.format(top_words[i]) , '{:<10}'.format(sentiment))
    
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
            
            top_dict[rank_set[i][0]] = [temp, temp2]

            top_word.append(temp)
            top_f.append(temp2)

        return top_dict
        
    def rank_list(self):

        #pull word from tokenization database
        cursor = self.pull_word()
        #turn off printing raw
        db_action.not_print_raw()

        total_list = []

        #append all the word from every tweet into total_list
        for doc in cursor:
            total_list += list(doc.values())[0]

        #counting the frequency of elements
        rank_dict = dict(collections.Counter(total_list))
        #sort from high to low
        rank_dict = dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))
        #create a list from word
        ranking_key = list(rank_dict.keys())
        #create a list from word frequency
        ranking_frequency = list(rank_dict.values())
        #ranking by frequency
        rank_set = list(enumerate(sorted(set(ranking_frequency), reverse=True), start=1))

        # print(rank_set)

        # print(self.rank_word(rank_set, ranking_key, ranking_frequency))

        #ranking by frequency but showing its sentiments
        self.sentiment_cal(self.rank_word( rank_set, ranking_key, ranking_frequency))
            
if __name__ == '__main__':

    # cProfile.run('Ranking().rank_list()')
    Ranking().rank_list()
