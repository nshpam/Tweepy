# coding=utf8
#import file
import config   #contain configuration of the application
import database_action

#import library
# nltk.download('stopwords')    #use one time for download nltk stopwords 
# nltk.download(' wordnet ')      #use one time for download nltk POS
import requests #use for API requesting
import time     #use for timer
from pythainlp.corpus import thai_stopwords #use for Thai stop word cleaning
from nltk.corpus import stopwords   #use for English stop word cleaning
from nltk import WordNetLemmatizer  #use for English normalization
from nltk.stem.porter import *  #use for stemming
from unidecode import unidecode
import datetime

db_action = database_action.DatabaseAction()

#connect to Lexto+ API
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
    def Filters(self, raw_list):

        if type(raw_list) != type(''):
            return 'Invalid data type'

        #split sentence
        raw_list = raw_list.split()
        clean_json = ''

        #list of splited sentence iteration
        for i in range(len(raw_list)):  
            word = raw_list[i]

            if self.FilterUrl(word):
                clean_json+=' '
                continue
            word = self.FilterNum(word)
            word = self.FilterSpecialChar(word)

            if word.strip() == '':
                continue
            clean_json += ' ' + word.strip()
            
        word = clean_json
        return word.lstrip().rstrip()

    #Filter url function
    def FilterUrl(self, raw_url):
        try :
            raw_url.index('https://')
            return True
        except:
            try:
                raw_url.index('http://')
                return True
            except:
                return False
            # return False

    #Filter number function
    def FilterNum(self, raw_text):

        if type(raw_text) != type(''):
            return 'Invalid data type'

        raw_text = ''.join(filter(lambda x: not x.isdigit(), raw_text.strip()))
        return raw_text
    
    def FilterSpecialChar(self, raw_text):

        if type(raw_text) != type(''):
            return 'Invalid data type'

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
        
        return temp_text.lower().lstrip().rstrip()
    
    # new function to filter out a specific keyword
    def FilterOutKeyword(self, text, keyword):
        filtered_text = ''
        words = text.split()

        for word in words:
            if word.lower() != keyword.lower():
                filtered_text += ' ' + word

        return filtered_text.strip()

#Tokenization function
class Tokenization():

    def __init__(self, count_untoken=0, count_token=0, cursor=None):
        self.count_untoken = count_untoken
        self.count_token = count_token
        self.cursor = cursor

    def IsMatch(self, cursor):
        #no keyword match
        if cursor.count() == 0:
            return False
        #keyword match
        return True

    def PullCleanByKeyword(self, keyword):
        db_action.not_print_raw() #turn off printing database status

    def PullCleanByTime(self):
        pass

    def PullTweets(self, keyword):
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)

        db_action.not_print_raw()
        
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        cursor = db_action.tweetdb_find(config.collection_name, collection, query_object)
        return cursor
    
    def TokenizationPrepare(self, doc):
        #filter url, numeric and special characters
        doc['text'] = FilterData().Filters(doc['text']).strip()
        #convert to dict
        doc_dict = dict(doc)
        #activate normalization
        doc_dict['norm'] = config.LextoPlus_Norm
        
        return doc_dict
    
    def TokenizationByTime(self, api_key, url, cursor, date_list):
        #start the timer
        tic = time.perf_counter()
        tokened_dict = {}

        #find by keyword already
        for doc in cursor:
            for date in date_list:
                #found the date to be tokenize
                if doc['date'].date() == date:
                    doc_dict = self.TokenizationPrepare(doc)

                    #connect with Lexto+ API
                    res = ConnectLextoPlus().ConnectApi(api_key, url, doc_dict)

                    try:
                        tokened_dict[doc['id']] = [doc['keyword'], doc['date'], FilterData().FilteredFromLexto(res.json())]
                        
                        #check if the data can be filter by Lexto+
                        if tokened_dict[doc['id']] == []:
                            print(doc_dict)
                            print(res.text)

                        self.count_token += 1
                    except:

                        self.count_untoken += 1
                        tokened_dict[doc['id']] = [doc['keyword'], doc['date'], doc['text'].split()]
                else:
                    continue
            time.sleep(0.1)

        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        print('TOTAL TOKENIZATION :', self.count_token + self.count_untoken)
        
        return tokened_dict

    def TokenizationByKeyword(self, api_key, url, cursor):
        #start the timer
        tic = time.perf_counter()
        tokened_dict = {}

        for doc in cursor:
            doc_dict = self.TokenizationPrepare(doc)

            #connect with Lexto+ API
            res = ConnectLextoPlus().ConnectApi(api_key, url, doc_dict)
            try:
                tokened_dict[doc['id']] = [doc['keyword'], doc['date'], FilterData().FilteredFromLexto(res.json())]
                        
                #check if the data can be filter by Lexto+
                if tokened_dict[doc['id']] == []:
                    print(doc_dict)
                    print(res.text)

                self.count_token += 1
            except:

                self.count_untoken += 1
                tokened_dict[doc['id']] = [doc['keyword'], doc['date'], doc['text'].split()]
            time.sleep(0.1)
                
        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        print('TOTAL TOKENIZATION :', self.count_token + self.count_untoken)

        return tokened_dict
    
# Read file from database
    def LextoPlusTokenization(self, api_key, url, keyword, date_list):

        print('Start Tokenization')
        #start the timer
        tic = time.perf_counter()

        tokened_dict = {}
        #database iteration

        cursor = self.PullTweets(keyword)
        #check the operation
        if date_list == ['keyword']:
            #perform tokenization by keyword
            tokened_dict = self.TokenizationByKeyword(api_key, url, cursor)
        
        #elif date_list == []:
        #     #check tweets database
        #     #sentiment
        #     print('extract') 
        else:
            #perform tokenization by time
            tokened_dict = self.TokenizationByTime(api_key, url, cursor, date_list)
        
        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        print('TOTAL TOKENIZATION :', self.count_token + self.count_untoken)

        return tokened_dict

#Clean Thai stopwords and English stopwords function
# Removing noise from the data
class CleanThaiAndEng():

    def cleaning(self, sentence):
        #clean thai word
        sentence = self.cleanThaiStopword(sentence)

        #clean english word
        sentence = self.cleanEnglishStopword(sentence)
        return sentence
    
    #Clean Thai stopwords function (use pythainlp)
    def cleanThaiStopword(self, sentence):

        #dictionary-based stopword
        stop_words = list(thai_stopwords())
        result = []

        #word iteration
        for word in sentence:

            #stopwords filter
            if word not in stop_words:
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

class Transform():

    def __init__(self, collection_name='', count_db=0, collection=None):
        self.collection_name = collection_name
        self.count_db = count_db
        self.collection = collection

    #check duplicate id in cleaned_data collection
    def check_cleaned_database(self, id):
        query_object = db_action.tweetdb_create_object(["id"],[id])
        cursor = db_action.tweetdb_find(self.collection_name, self.collection, query_object)
        return cursor
    
    def insert_cleaned_database(self, id, keyword, date, word):
        data_field = ['id','keyword','date','text']
        data_list = [id, keyword, date, word]
        clean_object = db_action.tweetdb_create_object(data_field, data_list)
        db_action.tweetdb_insert(self.collection_name, self.collection, clean_object)

    def perform(self, id_list, data_list):
        self.count_db = 0
        self.collection_name = config.collection_name_2
        self.collection = db_action.tweetdb_object(config.mongo_client, config.database_name, self.collection_name)

        for i in range(len(data_list)):
            self.count_db += 1
            word = data_list[i][2]
            word = Normailize().NormalizingEnglishword(word)
            word = CleanThaiAndEng().cleaning(word)

            if word != []:
                #check duplicate id in cleaned_data collection
                cursor = self.check_cleaned_database(id_list[i])

                #if not duplicate then insert
                if list(cursor) == []:
                    self.insert_cleaned_database(id_list[i], data_list[i][0], data_list[i][1], word)
                else:
                    print('duplicate data :', id_list[i])
            else:
                print('failed to insert :',word)
        
        print('TOTAL TWITTER INSERT TO DATABASE :',self.count_db)

# if __name__ == '__main__':

#     tweet_dict = Tokenization().LextoPlusTokenization(
#         config.LextoPlus_API_key,
#         config.LextoPlus_URL,
#         config.search_word
#     )

#     tweet_dict_keys = list(tweet_dict.keys())
#     tweet_dict_values = list(tweet_dict.values())

#     Transform().perform(tweet_dict_keys, tweet_dict_values)