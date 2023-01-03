import pymongo
import config
import requests
import json


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

        # print(raw_json)

        if raw_json == 0:
            return '0'

        for i in range(len(raw_json['types'])):
                if raw_json['types'][i] == 0 or raw_json['types'][i] == 1 or raw_json['types'][i] == 2:
                    if raw_json['tokens'][i].strip() != '':
                        self.temp_filtered.append(raw_json['tokens'][i].strip())
        self.filtered.append(self.temp_filtered)
        self.temp_filtered = []
        return self.filtered

    def LextoSetup(self):
        
        for doc in cursor:
            
            # print(doc)
            doc_dict = dict(doc)

            # return doc_dict
            doc_dict['norm'] = '1'
            # return doc_dict
            
            headers = {'Apikey': self.Apikey}
            res = requests.get(self.url,params=doc,headers=headers)


            try:
                raw = res.json()
                # print(raw)
            except json.JSONDecodeError:
                self.FilteredFromLexto(0)


            self.filtered = self.FilteredFromLexto(raw)

            # Close the connection to MongoDB when you're done.
            myclient.close()

        return self.filtered 

if __name__ == '__main__':
   print('filtered', ConnectLextoPlus().LextoSetup())  
    
    
