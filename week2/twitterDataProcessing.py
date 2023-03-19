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
            word = self.FilterHashtags(word)
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
    
    #Filter out the hashtags
    def FilterHashtags(self, raw_text):
        remove_word = []
        hashtags = raw_text.split('#')

        for tag in hashtags:
            if tag.startswith(' '):
                continue
            try: 
                hashtag = raw_text[raw_text.index(tag)-1]
                if hashtag == '#':
                    check_hashtags = tag.split()
                    filter_hashtags = tag
                    if len(check_hashtags)>1:
                        filter_hashtags = check_hashtags[0]
                    remove_word.append(hashtag+filter_hashtags)
            except:
                continue
        
        for word in remove_word:
            raw_text = raw_text.replace(word,'')
        return raw_text.lstrip().rstrip()

#Tokenization function
class Tokenization():

    def __init__(self, count_untoken=0, count_token=0, cursor=None):
        self.count_untoken = count_untoken
        self.count_token = count_token
        self.cursor = cursor

    def IsMatch(self, collection, query_object):
        #no keyword match
        if collection.count_documents(query_object) == 0:
            return False
        #keyword match
        return True

    #pull tweets by keyword
    def PullTweetsByKeyword(self, keyword):
        db_action.not_print_raw() #turn off printing database status

        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)
        #create query object
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        #query
        cursor = db_action.tweetdb_find(config.collection_name, collection, query_object)

        #check if have the keyword
        if not self.IsMatch(collection, query_object):
            return None
        return cursor

    def PullTweetsByTime(self, keyword, date_list):
        transform_dict = {} #storing the data that can transform
        extract_list = [] #storing the data that can't transform
        data_dict = {} #storing the data for transformation and extraction
        check_extract = [] #temparary storing date

        db_action.not_print_raw() #turn off printing database status

        #connect with tweets database
        #create collection
        collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)
        query_object = db_action.tweetdb_create_object(["keyword"], [keyword])
        cursor = db_action.tweetdb_find(config.collection_name, collection, query_object)

        #check if have the keyword
        if not self.IsMatch(collection, query_object):
            return None

        #pull all time from database
        for doc in cursor:
            for date in date_list:
                if doc['date'].date() == date:
                    transform_dict[doc['id']] = [doc['keyword'], doc['date'].date(), doc['text']]
                    check_extract.append(date)

        #check which date should be extract
        for date in date_list:
            if date not in check_extract:
                extract_list.append(date)
        
        #collect sentiment data and date to extract
        data_dict['transform'] = transform_dict
        data_dict['extract'] = extract_list

        return data_dict
    
    def TokenizationPrepare(self, doc):
        #filter url, numeric and special characters
        doc['text'] = FilterData().Filters(doc['text']).strip()
        #convert to dict
        doc_dict = dict(doc)
        #activate normalization
        doc_dict['norm'] = config.LextoPlus_Norm
        
        return doc_dict

    def TokenizationByKeyword(self, cursor):

        tokened_dict = {}

        #iterate all data in cursor
        for doc in cursor:
            #prepare data dict before tokenization
            doc_dict = self.TokenizationPrepare(doc)

            #perform a tokenization
            res = requests.get(config.LextoPlus_URL, headers={'Apikey':config.LextoPlus_API_key}, params=doc_dict)

            try:
                raw = res.json()

                #filter data
                filtered_raw = FilterData().FilteredFromLexto(raw)
                
                #collect data
                tokened_dict[doc['id']] = [doc['id'], doc['keyword'], doc['date'], filtered_raw]

                #check if the data is tokenized by Lexto+
                if tokened_dict[doc['id']] == []:
                    print(doc_dict)
                    print(res.text)
            
            except Exception as e:
                #collect data for insertion
                tokened_dict[doc['id']] = ['error']
                
                #print the error on console
                print('error:',e)
                print(doc_dict)

            #delay for Lexto+ API
            time.sleep(0.5)
        return tokened_dict

    def TokenizationByTime(self, tokened_raw):

        #each element in tokened_raw is added normalize already
        tokened_dict = {}

        #iterate data in tokened data
        for id in tokened_raw:
            
            #add normalize configuration before tokenization
            doc_dict = self.TokenizationPrepare({'text': tokened_raw[id][2]})  

            #perform a tokenization
            res = requests.get(config.LextoPlus_URL, headers={'Apikey':config.LextoPlus_API_key}, params=doc_dict)

            try:
                raw = res.json()

                #filter data
                filtered_raw = FilterData().FilteredFromLexto(raw)

                #collect data
                tokened_dict[id] = [id, tokened_raw[id][0], tokened_raw[id][1], filtered_raw]

                #check if the data is tokenized by Lexto+
                if tokened_dict[id] == []:
                    print(tokened_dict[id])
                    print(res.text)
            
            except Exception as e:
                #collect data for insertion
                tokened_dict[id] = ['error']
                
                #print the error on console
                print('error:',e)
                print(id, tokened_raw[id][0], tokened_raw[id][1], tokened_raw[id][2])
            
            #delay for Lexto+ API
            time.sleep(0.5)
        return tokened_dict

    def Perform(self, keyword, date_list, tokenize_type):
        tokened_dict = {}

        #tokenization by time
        if tokenize_type == 'time':
            #create data list for stokenization
            data_dict = self.PullTweetsByTime(keyword, date_list)

            #no keyword match
            if data_dict == None:
                tokened_dict['transform'] = []
                tokened_dict['extract'] = date_list
                return tokened_dict

            #perform tokenization by time
            tokened_dict['transform'] = self.TokenizationByTime(data_dict['transform'])
            tokened_dict['extract'] = data_dict['extract']
        #tokenization by keyword
        elif tokenize_type == 'keyword':
            #create cursor
            cursor = self.PullTweetsByKeyword(keyword)

            #no keyword match
            if cursor == None:
                tokened_dict['transform'] = []
                tokened_dict['extract'] = [keyword]
                return tokened_dict
            
            #perform the tokenization by keyword
            tokened_dict['transform'] = self.TokenizationByKeyword(cursor)
            tokened_dict['extract'] = []
        #invalid tokenization type
        else:
            return 'Invalid tokenization type'
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

if __name__ == '__main__':
    
    tokenization = Tokenization()

    # date_list = [datetime.datetime(2023, 1, 11).date(),
    #          datetime.datetime(2023, 1, 12).date(),
    #          datetime.datetime(2023, 1, 13).date(),
    #          datetime.datetime(2023, 1, 15).date()]

    # data_dict = tokenization.Tokenization(config.search_word, date_list, 'time')
    data_dict = tokenization.Perform(config.search_word, [], 'keyword')
    print(data_dict)

#     tweet_dict = Tokenization().LextoPlusTokenization(
#         config.LextoPlus_API_key,
#         config.LextoPlus_URL,
#         config.search_word
#     )

#     tweet_dict_keys = list(tweet_dict.keys())
#     tweet_dict_values = list(tweet_dict.values())

#     Transform().perform(tweet_dict_keys, tweet_dict_values)