import config
import pymongo

class DatabaseAction():
    
    def __init__(self, db_name='', col_name='', myclient=None, mydb=None, mycol=None, cursor=None, count=0, arp=True, cmd=None, history=True):
        # self.db_name = db_name
        # self.col_name = col_name
        self.myclient = myclient
        self.mydb = mydb
        self.mycol = mycol
        self.cursor = cursor
        self.count = count
        self.arp = arp
        self.cmd = cmd
        self.history = history

    def print_raw(self):
        self.arp = True
        return self.arp
    
    def not_print_raw(self):
        self.arp = False
        return self.arp
    
    def collect_history(self):
        self.history = True
        return self.history
    
    def not_collect_history(self):
        self.history = False
        return self.history
    
    #connect to database
    def tweetdb_object(self, mongoclient_to_connect, db_to_connect, col_to_connect):
        self.db_name = db_to_connect
        self.col_name = col_to_connect
        
        try :
            self.myclient = pymongo.MongoClient(mongoclient_to_connect)
            self.mydb = self.myclient[self.db_name]
            self.mycol = self.mydb[self.col_name]
        except Exception as e:
            print(e)
            return 'Failed to Connect MongoDB'
        else: #run when no error was raised     
            if self.arp:
                print('Database :', self.mydb.name)
                print('Collection :', self.mycol.name)

            return self.mycol
    
    #universal create object
    def tweetdb_create_object(self, data_field, data_list):

        data_dict = {}

        try:
            if len(data_field) != len(data_list):
                return 'Amount of key and value not match'
            for i in range(len(data_field)):

                if data_field[i] in data_field[:i]:
                    return 'Duplicate Keys'

                if self.arp:
                    print(data_field[i],':',data_list[i])
                try:
                    data_dict[data_field[i]] = data_list[i]
                except Exception as e:
                    print(e)
                    return 'Incorrect Data'
        except:
            return 'Failed to create object'
        
        return data_dict

    #show all data in every collection
    def tweetdb_showall_collection(self, col_list):

        if type(col_list) != type([]):
            return 'Invalid Collection List'

        data_dict = {}
        amount_list = []
        temp_list = []

        for i in range(len(col_list)):

            if type(col_list[i]) != type([]):
                return 'Invalid Collection'

            self.cursor = col_list[i].find()

            for doc in self.cursor:
                temp_list.append(doc)
                if self.arp:
                    print(doc)
                self.count +=1

            amount_list.append(self.count)
            data_dict[col_list[i].name] = temp_list
            self.count = 0
            temp_list = []

        for i in range(len(amount_list)):
            print('TOTAL of %s :' %self.mydb.list_collection_names()[i], amount_list[i])
       
        return data_dict

    #show all data in specified collection
    def tweetdb_show_collection(self, col_name, col_to_show, query_object):

        self.cursor = col_to_show.find({},query_object)

        if self.arp:
            print('DATABASE NAME : %s'%config.database_name)
            print('COLLECTION NAME : %s'%col_name)

        return self.cursor
    
    #query database
    def tweetdb_find(self, col_name, col_to_find, query_object):

        self.cursor = col_to_find.find(query_object)

        if self.arp:
            print('SEARCH FROM : %s'%col_name)
            print('FOUND :', list(self.cursor))
        return self.cursor
    
    #update database
    def tweetdb_update(self, col_name, col_to_update, data_to_update, query_field, query):

        #value for update
        update_dict = {"$set":data_to_update}

        #update database base on id
        self.cmd = col_to_update.update_one({query_field:query}, update_dict)

        if self.arp:
            print('UPDATE', update_dict, 'to %s'%col_name)

        return self.cmd
    
    #insert database
    def tweetdb_insert(self, col_name, col_to_insert, data_to_insert):

        #command for insert object to mongodb
        #insert to the specified collection
        self.cmd = col_to_insert.insert_one(data_to_insert)

        if self.arp:
            print('INSERT', data_to_insert, 'to %s'%col_name)

        return self.cmd
    
    #delete all database
    def tweetdb_delete_all(self):

        for col in self.mydb.list_collection_names():
            collection = self.tweetdb_object(config.mongo_client, config.database_name, col)
            collection.delete_many({})
            
            print('CLEAR ALL DATA IN %s' %col)

    #delete database collection by collection
    def tweetdb_delete_collection(self, col_name, col_to_delete):

        self.cmd = col_to_delete.delete_many({})
        
        print('CLEAR ALL DATA IN %s' %col_name)
        
        return self.cmd
    
    #history log
    def tweetdb_history(self, action, last_id):
        
        history_db = self.tweetdb_object(config.mongo_client, config.database_name, config.history_db)
        collect_history = history_db.insert_one({
            'action':action,
            'last_id': last_id
            })

        if self.arp:
            print('COLLECT HISTORY : %s'%action)
            
        return collect_history
        
if __name__ == '__main__':
    db_action = DatabaseAction()
    
    collection = db_action.tweetdb_object('asdasf', 'asdhjvfjh', 'ladfjgj')
    # print(db_action.mycol.name)
    # query_object = db_action.tweetdb_create_object(['id'], ['1612808365272608769'])
    # db_action.tweetdb_find(config.collection_name, collection ,query_object)

    # db_action.tweetdb_delete_collection(config.collection_name_5, collection)

    # db_action.tweetdb_delete_all()
    
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
    # db_action.tweetdb_find(config.collection_name, collection, "id", "1611421440200552448")

    # data_field = ["favorite_count", "retweet_count"]
    # data_list = [20,30]
    # data_dict_to_update = db_action.tweetdb_create_object(data_field, data_list)
    # print(data_dict_to_update)

    # db_action.tweetdb_update(config.collection_name, collection, data_dict_to_update, 'id', '1612334817252896775')

    # data_field = ["id", "username", "date", "time", "favorite_count", "retweet_count"]
    # data_list = ['1', 'test', '14-01-2023', '12:34', '0', '0']
    # data_to_insert = db_action.tweetdb_create_object(data_field, data_list)
    # db_action.tweetdb_insert(config.collection_name_5, collection, data_to_insert)