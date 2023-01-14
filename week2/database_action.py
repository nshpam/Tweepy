import config
import pymongo

#connect to mongodb server with pymongo
myclient = pymongo.MongoClient(config.mongo_client)
#choose database name
mydb = myclient[config.database_name]
#choose collection name
# mycol = mydb[config.collection_name]
mycol = mydb[config.collection_name_4]

class DatabaseAction():
    
    def __init__(self, db_name='', col_name='', myclient=None, mydb=None, mycol=None, cursor=None, count=0, arp=True):
        self.db_name = db_name
        self.col_name = col_name
        self.myclient = myclient
        self.mydb = mydb
        self.mycol = mycol
        self.cursor = cursor
        self.count = count
        self.arp = arp
    
    def not_print_raw(self):
        self.arp = False
        return self.arp
    
    #connect to database
    def tweetdb_object(self, mongoclient_to_connect, db_to_connect, col_to_connect):
        self.db_name = db_to_connect
        self.col_name = col_to_connect

        self.myclient = pymongo.MongoClient(mongoclient_to_connect)
        self.mydb = self.myclient[self.db_name]
        self.mycol = self.mydb[self.col_name]

        return self.mycol

    #show all data in every collection
    def tweetdb_showall_collection(self, col_list):

        amount_list = []

        for i in range(len(col_list)):
            self.cursor = col_list[i].find()

            for doc in self.cursor:

                if self.arp:
                    print(doc)
                self.count +=1

            amount_list.append(self.count)
            self.count = 0

        for i in range(len(amount_list)):
            print('TOTAL of %s :' %self.mydb.list_collection_names()[i], amount_list[i])

    #show all data in specified collection
    def tweetdb_show_collection(self, col_name, col_to_show):

        self.cursor = col_to_show.find()

        for doc in self.cursor:
            if self.arp:
                print(doc)
            self.count +=1

        print('TOTAL of %s :' %col_name, self.count)
        self.count = 0
    
    #query database
    def tweetdb_findall(self, col_name, col_to_find, field_to_find, query):

        self.cursor = col_to_find.find({field_to_find : query})

        print('SEARCH FROM : %s'%col_name)
        print('FOUND :', list(self.cursor))
        return self.cursor


if __name__ == '__main__':
    db_action = DatabaseAction()

    collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)
    
    # collection_list = [
    #     db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name),
    #     db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_2),
    #     db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_3),
    #     db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_4),
    #     db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name_4)
    # ]
    # db_action.not_print_raw()
    # db_action.tweetdb_showall_collection(collection_list)

    # db_action.tweetdb_show_collection(config.collection_name ,collection)
    # db_action.tweetdb_findall(config.collection_name, collection, "id", "1611421440200552448")