import pymongo
import config
import requests
import time
import tweepy_main

from pythainlp.corpus import thai_stopwords
import nltk 
# nltk.download('stopwords')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk.stem.porter import *

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)

#database name
mydb = myclient[config.database_name]
# #collection name
mycol_1 = mydb[config.collection_name]
mycol_2 = mydb[config.collection_name_2]
# #select only text
cursor = mycol_1.find({},{ "_id": 0, "text": 1})

class FilterData():

    def __init__(self, filtered=[], temp_filtered=[]):
        self.filtered = filtered
        self.temp_filtered = temp_filtered

    def FilteredFromLexto(self, raw_json):
        if raw_json == 0:
            return '0'

        for i in range(len(raw_json['types'])):
                if raw_json['types'][i] == 0 or raw_json['types'][i] == 1 or raw_json['types'][i] == 2:
                    if raw_json['tokens'][i].strip() != '':
                        self.temp_filtered.append(raw_json['tokens'][i].strip().lower())
                    
        self.filtered.append(self.temp_filtered)
        self.temp_filtered = []
        return self.filtered

    def FilterUrlAndFilterNum(self, raw_list):

        raw_list = raw_list.split()
        clean_json = ''

        for i in range(len(raw_list)):
            try:
                self.FilterUrl(raw_list[i])
            except ValueError:
                clean_json += ' '+ self.FilterNum(raw_list[i])
        return clean_json

    def FilterUrl(self, raw_url):
        raw_url = raw_url.index('https://')
        return raw_url

    def FilterNum(self, raw_text):
        raw_text = ''.join(filter(lambda x: not x.isdigit(), raw_text))
        return raw_text

class Tokenization():
    
# Read file from database
    def LextoPlusTokenization(self, api_key, url):
        print('Start Tokenization')
        #start the timer
        tic = time.perf_counter()

        filtered = []
        for doc in cursor:
            doc['text'] = FilterData().FilterUrlAndFilterNum(doc['text'])
            doc_dict = dict(doc)

            doc_dict['norm'] = '1'
            
            headers = {'Apikey': api_key}
            res = requests.get(url,params=doc,headers=headers)            

            if res.text != '' and res.status_code==200:
                raw = res.json()
                filtered = FilterData().FilteredFromLexto(raw)

        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        return filtered

class CleanThaiAndEng():
# Removing noise from the data
    
    def cleanThaiStopword(self, sentence):
        stop_word = list(thai_stopwords())
        result = []
        for word in sentence:
            if word not in stop_word:
                result.append(word)
        return result
        
    def cleanEnglishStopword(self, sentence):
        stop_words = stopwords.words('english')
        result = []
        for word in sentence:
            if word.lower() not in stop_words:
                result.append(word)
        return result
    
class Normailize():

    # Normalizing English words
    def NormalizingEnglishword(self, sentence):
        lemmatizer = WordNetLemmatizer()
        nltk_lemma_list = []
        pos_list = ['n','v','a','r','s']
        for word in sentence:
            if word != '':
                for mode in pos_list:
                    temp = lemmatizer.lemmatize(word,pos=mode)
                    word = temp
                    
                nltk_lemma_list.append(temp)
        return nltk_lemma_list
    
class CreateDatabaseObject():

    def create_db_object(self, cleaned_list):

        db_object = {
            'sentiment_data': cleaned_list
        }

        return db_object
    
        
if __name__ == '__main__':

    tweet_list = Tokenization().LextoPlusTokenization(
        config.LextoPlus_API_key,
        config.LextoPlus_URL
    )

    print('TOTAL TWITTER :',len(tweet_list))
    
    # Close the connection to MongoDB when you're done.
    

    print('Start Word Cleaning and Word Normalization')
    
    tic = time.perf_counter()
    for word in tweet_list:
        word = CleanThaiAndEng().cleanThaiStopword(word)
        word = CleanThaiAndEng().cleanEnglishStopword(word)
        word = Normailize().NormalizingEnglishword(word)

        tweepy_main.PullTwitterData().insert_database(
            CreateDatabaseObject().create_db_object(word), 
            mycol_2)
    
    #stop the timer
    toc = time.perf_counter()

    #display total work time of this thread
    print(f"RUN TIME : {toc - tic:0.4f} seconds")

    print('TOTAL TWITTER :',len(tweet_list))

    myclient.close()
        
        
          
    