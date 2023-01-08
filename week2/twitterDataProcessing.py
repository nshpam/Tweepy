import pymongo
import config
import requests

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
mycol = mydb[config.collection_name]
# #select only text
cursor = mycol.find({},{ "_id": 0, "text": 1})

class ConnectLextoPlus():
    #import Api LexTo+
    Apikey = 'Ex0WSb2UFAyfDXRU8vLwkeR04N6e58Tq' 
    url = 'https://api.aiforthai.in.th/lextoplus'
    filtered = []
    temp_filtered = []

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

    def FilterUrl(self, raw_list):
        raw_split = raw_list.split()
        no_url_json = ''
                
        for i in range(len(raw_split)):
            try:
                raw_split[i].index('https://')
            except ValueError:
                no_url_json += ' '+ self.FilterNum(raw_split[i])
        return no_url_json

    def FilterNum(self, raw_text):
        raw_text = ''.join(filter(lambda x: not x.isdigit(), raw_text))
        return raw_text

    
# Read file from database
    def LextoSetup(self):
        
        for doc in cursor:

            doc['text'] = self.FilterUrl(doc['text'])
            doc_dict = dict(doc)

            doc_dict['norm'] = '1'
            
            headers = {'Apikey': self.Apikey}
            res = requests.get(self.url,params=doc,headers=headers)

            if res.text != '':

                raw = res.json()
           
                self.filtered = self.FilteredFromLexto(raw)

        return self.filtered 

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
    
        
if __name__ == '__main__':
#     # print('filtered', ConnectLextoPlus().LextoSetup())  
    tweet_list = ConnectLextoPlus().LextoSetup()

    print('count :',tweet_list)

    # Close the connection to MongoDB when you're done.
    myclient.close()
    print(tweet_list)
    for word in tweet_list:
        word = ConnectLextoPlus().cleanThaiStopword(word)
        word = ConnectLextoPlus().cleanEnglishStopword(word)
        print(ConnectLextoPlus().NormalizingEnglishword(word))
    # for word in tweet_list:
        
        
        
          
    