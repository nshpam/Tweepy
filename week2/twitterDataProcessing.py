# coding=utf8
#import file
import config   #contain configuration of the application
import tweepy_main  #contain method for scraping twitter

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

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)

#database name
mydb = myclient[config.database_name]

#collection name
mycol_1 = mydb[config.collection_name]
mycol_2 = mydb[config.collection_name_2]
mycol_3 = mydb[config.collection_name_3]
mycol_4 = mydb[config.collection_name_4]

#select only text
# cursor = mycol_1.find({},{ "_id": 0, "text": 1})
cursor = mycol_4.find({},{ "_id": 0, "id": 1 ,"text": 1})

#Filter class
class FilterData():

    #initialize variables
    def __init__(self, filtered=[], temp_filtered=[]):
        self.filtered = filtered
        self.temp_filtered = temp_filtered

    #Filter out unnecessary data (no meanning word, conjunction and etc...)
    def FilteredFromLexto(self, raw_json):

        #iterate types from tokenization dict
        for i in range(len(raw_json['types'])):

            #filter out no meaning word, conjunction, emoji, special characters
            if raw_json['types'][i] == 0 or raw_json['types'][i] == 1 or raw_json['types'][i] == 2:
                if raw_json['tokens'][i].strip() != '':

                    #append filtered data in temp list
                    self.temp_filtered.append(raw_json['tokens'][i].strip().lower())
        
        #append all data
        self.filtered.append(self.temp_filtered)
        self.temp_filtered = []
        return self.filtered
    
    def ThaiCleansing(self, text_to_clean):
        #connect to ThaiCleansing API
        headers = {'Apikey': config.LextoPlus_API_key}
        res = requests.get(config.Thai_Cleasing,params=text_to_clean,headers=headers)
        res = res.json()
        return res    

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
                    # word = self.ThaiCleansing({'text':word})
                    # clean_json += ' '+ word['cleansing_text']
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

        for list_word in raw_text.split():

            temp_dict[list_word] = list_word.encode('ascii','namereplace').decode('utf-8').split('\\N')
            temp_dict[list_word] = temp_dict[list_word][1:]

            for word in temp_dict[list_word]:
                if 'THAI' not in word and '{' in word and '}' in word:
                    if unidecode(list_word) not in temp_text.split():
                        temp_text += ' ' + unidecode(list_word)
                    continue
                temp_text += ' ' + list_word
                break
        
        return temp_text

#Tokenization function
class Tokenization():

    def __init__(self, count_untoken=0, count_token=0):
        self.count_untoken = count_untoken
        self.count_token = count_token
    
# Read file from database
    def LextoPlusTokenization(self, api_key, url):

        print('Start Tokenization')
        #start the timer
        tic = time.perf_counter()

        tokened_dict = {}
        count = 0
        #database iteration
        for doc in cursor:

            count += 1

            #send data to filter url and numeric
            doc['text'] = FilterData().FilterUrlAndFilterNum(doc['text']).strip()
            doc['text'] = FilterData().FilterSpecialChar(doc['text'])

            #convert filtered data to dictionary
            doc_dict = dict(doc)

            #activate normalization
            doc_dict['norm'] = config.LextoPlus_Norm

            #connect with Lexto+ API
            headers = {'Apikey': api_key}
            res = requests.get(url,params=doc,headers=headers)     

            #scan response
            if res.text != '' and res.status_code == 200:
                raw = res.json()
                tokened_dict[doc['id']] = FilterData().FilteredFromLexto(raw)
                self.count_token += 1
            else:
                # print('unable to tokenization',doc)
                tokened_dict[doc['id']] = 'unable to tokenization'
                self.count_untoken += 1

            if count == 2:
                print(tokened_dict)
                
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

    # print(list(tweet_dict.values())[:3])

    # FilterData().FilterUrlAndFilterNum()
    tweet_dict_keys = list(tweet_dict.keys())
    tweet_dict_values = list(tweet_dict.values())

    print('DATABASE INSERTION')

    # print(tweet_dict_keys[0],tweet_dict_values[0])

    # for i in range(len(tweet_dict_values)):
    #     print(tweet_dict_keys[i],tweet_dict_values[i])
    #     # print(CreateDatabaseObject().create_db_object(tweet_dict_keys[i], tweet_dict_values[i]))
    #     break
        # tweepy_main.PullTwitterData().insert_database(
        #         CreateDatabaseObject().create_db_object(tweet_dict_keys[i], tweet_dict_values[i]),
        #         mycol_3)

    print('TOTAL TWITTER INSERT TO DATABASE :',len(tweet_dict))
    
    # # Close the connection to MongoDB when you're done.
    

    # print('Start Word Cleaning and Word Normalization')
    
    # tic = time.perf_counter()
    # for word in tweet_list:
    #     word = CleanThaiAndEng().cleanThaiStopword(word)
    #     word = CleanThaiAndEng().cleanEnglishStopword(word)
    #     word = Normailize().NormalizingEnglishword(word)

    #     tweepy_main.PullTwitterData().insert_database(
    #         CreateDatabaseObject().create_db_object(word), 
    #         mycol_2)
    
    # #stop the timer
    # toc = time.perf_counter()

    # #display total work time of this thread
    # print(f"RUN TIME : {toc - tic:0.4f} seconds")

    # print('TOTAL TWITTER :',len(tweet_list))

    # myclient.close()