import pymongo
import config
import requests

#import Api LexTo+
Apikey = 'Ex0WSb2UFAyfDXRU8vLwkeR04N6e58Tq' 
# url = 'https://api.aiforthai.in.th/tlexplus' 
url = 'https://api.aiforthai.in.th/lextoplus' #Host 

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

    def FilteredFromLexto(self, raw_json):
        for i in range(len(raw_json['types'])):
                if raw_json['types'][i] == 0 or raw_json['types'][i] == 1:
                    if raw_json['tokens'][i].strip() != '':
                        self.filtered.append(raw_json['tokens'][i].strip())
        return self.filtered
    def LextoSetup(self):

        for doc in cursor:
            
            doc_dict = dict(doc)
            doc_dict['norm'] = '1'
            
            headers = {'Apikey': self.Apikey}
            res = requests.get(self.url,params=doc_dict,headers=headers)
            raw = res.json()

            self.filtered = self.FilteredFromLexto(raw)

            # Close the connection to MongoDB when you're done.
            myclient.close()

        return self.filtered 

if __name__ == '__main__':
   print('filtered', ConnectLextoPlus().LextoSetup())  
    
    
