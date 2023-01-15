# coding=utf8
#import file
import config   #contain configuration of the application
import tweepy_main  #contain method for scraping twitter
import database_action

#import library
# nltk.download('stopwords')    #use one time for download nltk stopwords 
# nltk.download(' wordnet ')      #use one time for download nltk POS
import pymongo  #use for connecting to mongodb
import requests #use for API requesting
import time     #use for timer
from pythainlp.corpus import thai_stopwords #use for Thai stop word cleaning
from nltk.corpus import stopwords   #use for English stop word cleaning
from nltk import WordNetLemmatizer  #use for English normalization
from nltk.stem.porter import *  #use for stemming
from unidecode import unidecode

db_action = database_action.DatabaseAction()

class ConnectLextoPlus():

    def ConnectApi(self, api_key, url_to_send, data_dict):
        headers = {'Apikey' : api_key}
        res = requests.get(url_to_send,params=data_dict,headers=headers)
        return res


#Filter class
class FilterData():

    #Filter out unnecessary data (no meanning word, conjunction and etc...)
    def FilteredFromLexto(self, raw_json):

        filtered = []
        temp_filtered = []

        #iterate types from tokenization dict
        for i in range(len(raw_json['types'])):

            #filter out no meaning word, conjunction, emoji, special characters
            if raw_json['types'][i] == 0 or raw_json['types'][i] == 1 or raw_json['types'][i] == 2:
                if raw_json['tokens'][i].strip() != '':

                    #append filtered data in temp list
                    temp_filtered.append(raw_json['tokens'][i].strip().lower())
        
        #append all data
        filtered = temp_filtered
        return filtered

    #Filter URL and numeric data funciton
    def FilterUrlAndFilterNum(self, raw_list):

        #split sentence
        raw_list = raw_list.split()
        clean_json = ''

        #list of splited sentence iteration
        for i in range(len(raw_list)):
            word = raw_list[i]
            
            #Filter URL
            try:
                self.FilterUrl(word)
            
            #Filter Number
            except ValueError:
                if raw_list[i] != '':
                    word = self.FilterNum(word)
                    clean_json += ' ' + word
        return clean_json

    #Filter url function
    def FilterUrl(self, raw_url):
        raw_url = raw_url.index('https://')
        return raw_url

    #Filter number function
    def FilterNum(self, raw_text):
        raw_text = ''.join(filter(lambda x: not x.isdigit(), raw_text.strip()))
        return raw_text
    
    def FilterSpecialChar(self, raw_text):
        temp_dict = {}
        temp_text = ''
        regex = re.compile('[@_!#$%^&*()<>?/\|~:]')

        for list_word in raw_text.split():

            temp_dict[list_word] = list_word.encode('ascii','namereplace').decode('utf-8').split('\\N')

            for word in temp_dict[list_word]:
                if word == '':
                    continue

                if regex.search(list_word) != None:
                        remove_char = regex.search(list_word).group()
                        list_word = list_word.replace(remove_char,"")
                    
                if 'THAI' not in word and '{' in word and '}' in word:
                    
                    if unidecode(list_word) not in temp_text.split() and unidecode(list_word).isalnum():
                        temp_text += ' ' + unidecode(list_word)
                    break

                elif list_word not in temp_text.split():
                        temp_text += ' ' + list_word
        
        return temp_text

#Tokenization function
class Tokenization():

    def __init__(self, count_untoken=0, count_token=0, cursor=None):
        self.count_untoken = count_untoken
        self.count_token = count_token
        self.cursor = cursor
    
    def ScanRawData(self, raw_object):
        if raw_object.text != '' and raw_object.status_code == 200:
            raw_json = raw_object.json()
            return raw_json
        else:
            return None
    
# Read file from database
    def LextoPlusTokenization(self, api_key, url):

        print('Start Tokenization')
        #start the timer
        tic = time.perf_counter()

        tokened_dict = {}
        #database iteration

        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

        db_action.not_print_raw()

        data_field = ["_id", "id", "text"]
        data_list = [0, 1, 1]
        query_object = db_action.tweetdb_create_object(data_field, data_list)
        cursor = db_action.tweetdb_show_collection(config.collection_name, collection, query_object)

        for doc in cursor:

            #send data to filter url and numeric
            doc['text'] = FilterData().FilterUrlAndFilterNum(doc['text']).strip()
            doc['text'] = FilterData().FilterSpecialChar(doc['text'])

            #convert filtered data to dictionary
            doc_dict = dict(doc)

            #activate normalization
            doc_dict['norm'] = config.LextoPlus_Norm

            #connect with Lexto+ API
            res = ConnectLextoPlus().ConnectApi(api_key, url, doc_dict)     

            try:
                tokened_dict[doc['id']] = FilterData().FilteredFromLexto(res.json())
                
                if tokened_dict[doc['id']] == []:
                    print(doc_dict)
                    print(res.text)

                self.count_token += 1
            except:

                self.count_untoken += 1
                tokened_dict[doc['id']] = doc['text'].split()
            
            time.sleep(1)
                
        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        print('TOTAL TOKENIZATION :', self.count_token + self.count_untoken)

        return tokened_dict

#Clean Thai stopwords and English stopwords function
# Removing noise from the data
class CleanThaiAndEng():
    
    #Clean Thai stopwords function (use Lexto+)
    def cleanThaiStopword(self, sentence):

        #dictionary-based stopword
        stop_word = list(thai_stopwords())
        result = []

        #word iteration
        for word in sentence:

            #stopwords filter
            if word not in stop_word:
                result.append(word)
        return result
    
    #Clean English stopwords function (use nltk)
    def cleanEnglishStopword(self, sentence):

        #dictionary-based stopword
        stop_words = stopwords.words('english')
        result = []

        #word iteration
        for word in sentence:

            #stopwords filter
            if word.lower() not in stop_words:
                result.append(word)
        return result

#Normalization function
class Normailize():

    # Normalizing English words
    def NormalizingEnglishword(self, sentence):
        lemmatizer = WordNetLemmatizer()
        nltk_lemma_list = []

        #normalization settings ( n (noun) | v (verb) | a (adjective) | r (adverb) | s (satellite adjective) )
        #POS tag (part-of-speech)
        pos_list = ['n','v','a','r','s']
        for word in sentence:
            if word != '':
                for mode in pos_list:
                    temp = lemmatizer.lemmatize(word,pos=mode)
                    word = temp
                    
                nltk_lemma_list.append(temp)
        return nltk_lemma_list
    
class CreateDatabaseObject():

    def create_db_object(self, uniqe_id, cleaned_list):

        db_object = {
            'id' : uniqe_id,
            'sentiment_data': cleaned_list
        }

        return db_object
    
        
if __name__ == '__main__':

    tweet_dict = Tokenization().LextoPlusTokenization(
        config.LextoPlus_API_key,
        config.LextoPlus_URL
    )

    tweet_dict_keys = list(tweet_dict.keys())
    tweet_dict_values = list(tweet_dict.values())

    count_db = 0

    for i in range(len(tweet_dict_values)):

        count_db+=1
        word = tweet_dict_values[i]

        word = CleanThaiAndEng().cleanThaiStopword(word)
        word = CleanThaiAndEng().cleanEnglishStopword(word)
        word = Normailize().NormalizingEnglishword(word)

        if word != []:
            collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2)
            clean_object = db_action.tweetdb_create_object([tweet_dict_keys[i]], [word])
            db_action.tweetdb_insert(config.collection_name_2, collection, clean_object)

    print('TOTAL TWITTER INSERT TO DATABASE :',count_db)