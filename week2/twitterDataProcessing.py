#import file
import config   #contain configuration of the application
import tweepy_main  #contain method for scraping twitter

#import library
import pymongo  #use for connecting to mongodb
import requests #use for API requesting
import time     #use for timer
from pythainlp.corpus import thai_stopwords #use for Thai stop word cleaning
# nltk.download('stopwords')    #use one time for nltk downloaing
# nltk.download('wordnet')      #use one time for nltk downloading
from nltk.corpus import stopwords   #use for English stop word cleaning
from nltk import WordNetLemmatizer  #use for English normalization
from nltk.stem.porter import *  #use for stemming

#connect to mongodb with pymongo
myclient = pymongo.MongoClient(config.mongo_client)

#database name
mydb = myclient[config.database_name]

#collection name
mycol_1 = mydb[config.collection_name]
mycol_2 = mydb[config.collection_name_2]

#select only text
cursor = mycol_1.find({},{ "_id": 0, "text": 1})

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

    #Filter URL and numeric data funciton
    def FilterUrlAndFilterNum(self, raw_list):

        #split sentence
        raw_list = raw_list.split()
        clean_json = ''

        #list of splited sentence iteration
        for i in range(len(raw_list)):

            #Filter URL
            try:
                self.FilterUrl(raw_list[i])
            
            #Filter Number
            except ValueError:
                clean_json += ' '+ self.FilterNum(raw_list[i])
        return clean_json

    #Filter url function
    def FilterUrl(self, raw_url):
        raw_url = raw_url.index('https://')
        return raw_url

    #Filter number function
    def FilterNum(self, raw_text):
        raw_text = ''.join(filter(lambda x: not x.isdigit(), raw_text))
        return raw_text

#Tokenization function
class Tokenization():
    
# Read file from database
    def LextoPlusTokenization(self, api_key, url):

        print('Start Tokenization')
        #start the timer
        tic = time.perf_counter()

        filtered = []

        #database iteration
        for doc in cursor:

            #send data to filter url and numeric
            doc['text'] = FilterData().FilterUrlAndFilterNum(doc['text'])

            #convert filtered data to dictionary
            doc_dict = dict(doc)

            #activate normalization
            doc_dict['norm'] = config.LextoPlus_Norm

            #connect with Lexto+ API
            headers = {'Apikey': api_key}
            res = requests.get(url,params=doc,headers=headers)            

            #scan response
            if res.text != '' and res.status_code==200:
                raw = res.json()
                filtered = FilterData().FilteredFromLexto(raw)

        #stop the timer
        toc = time.perf_counter()

        #display total work time of this thread
        print(f"RUN TIME : {toc - tic:0.4f} seconds")
        return filtered

#Clean Thai stopwords and English stopwords function
# Removing noise from the data
class CleanThaiAndEng():
    
    #Clean Thai stopwords function (use Lexto+)
    def cleanThaiStopword(self, sentence):
        stop_word = list(thai_stopwords())
        result = []
        for word in sentence:
            if word not in stop_word:
                result.append(word)
        return result
    
    #Clean English stopwords function (use nltk)
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