import unittest
from unittest.mock import patch, MagicMock
import database_action
from  collections import namedtuple
import pymongo

class FakeMongoDB():

    def __init__(self):
        self.data = {}
        self.client_data = ()
    
    # @patch('pymongo.MongoClient')
    def connect_to_mongoclient(self, mock_client):
        key_tuple = namedtuple('key_tuple', ['host', 'document_class', 'tz_aware', 'connect'])

        if mock_client == 'mongodb://localhost:27017/':
            self.client_data = key_tuple(
                host=['localhost:27017'], 
                document_class=dict, 
                tz_aware= False, #timezone aware
                connect= True)
        else:
            self.client_data = key_tuple(
                host=['localhost:27017'], 
                document_class=dict, 
                tz_aware= False, #timezone aware
                connect= False)
        
        return self.client_data
    # collection = db_action.tweetdb_object(config.mongo_client, config.database_name, config.collection_name)


class TestDatabaseActions(unittest.TestCase):
    
    #mock data for current database
    mongo_client = 'mongodb://localhost:27017/'
    mongo_db = 'twitter_data'
    mongo_col = 'tweets'
    mongo_all_col = ['tokenization', 'temp_tweets', 'tweets', 'tweet_history', 'temp_tokenization', 'sentiment']
    db_action = database_action.DatabaseAction()
    db_action.not_print_raw()

    #test tweetdb_object
    #---correct arguments case---

    #test if function were called with the specific arguments
    @patch('pymongo.MongoClient')
    def test_tweetdb_object_MongoClient_1(self, mock_client):
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
        mock_client.assert_called_with(self.mongo_client) #first argument
        mock_client().__getitem__.assert_called_with(self.mongo_db) #second argument
        mock_client().__getitem__().__getitem__.assert_called_with(self.mongo_col) #third argument
    
    #test if connect to the correct database
    def test_tweetdb_object_MongoDB_1(self):
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
        assert self.db_action.mydb.name == self.mongo_db
        assert self.db_action.mydb.list_collection_names() == self.mongo_all_col
    
    #test if connect to the correct collection
    def test_tweetdb_object_MongoCol_1(self):
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
        assert self.db_action.mycol.name == self.mongo_col

    #test if print_raw was called in tweetdb_object
    def test_not_print_raw_tweetdb_object(self):
        with patch('database_action.DatabaseAction.print_raw') as mock_tweetdb_object:
            self.db_action.print_raw()
            self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
            mock_tweetdb_object.assert_called_once()
        self.db_action.print_raw()
    
    #---incorrect arguments case---

    #incorrect mongoclient_to_connect
    def test_tweetdb_object_MongoClient_2(self):
        client = self.db_action.tweetdb_object(1, self.mongo_db, self.mongo_col)
        assert client == 'Failed to Connect MongoDB'
    
    #incorrect db_to_connect
    def test_tweetdb_object_MongoDB_2(self):
        client = self.db_action.tweetdb_object(self.mongo_client, 1, self.mongo_col)
        assert client == 'Failed to Connect MongoDB'

    #incorrect col_to_connect
    def test_tweetdb_object_MongoCol_2(self):
        client = self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, 1)
        assert client == 'Failed to Connect MongoDB'
    
    #all incorrect
    def test_tweetdb_object_AllMongo(self):
        client = self.db_action.tweetdb_object(1, 2, 3)
        assert client == 'Failed to Connect MongoDB'

    #test tweetdb_create_object

    #correct field_list and data_list
        
    #test if tweetdb_create_object can create the correct object
    def test_tweetdb_create_object(self):
        self.db_action.not_print_raw()
        data_field = ['test1','test2']
        data_list = [1,2]
        expect_object = {'test1':1, 'test2':2}

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == expect_object
    
    #incorrect field_list but correct data_list
    #incorrect keys
    def test_tweetdb_create_object_1(self):
        self.db_action.not_print_raw()
        data_field = [['test1'],['test2']]
        data_list = [1,2]

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == 'Incorrect Data'
    
    #duplicate keys
    def test_tweetdb_create_object_2(self):
        self.db_action.not_print_raw()
        data_field = ['test1','test1','test2']
        data_list = [1,2,3]

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == 'Duplicate Keys'
    
    #incorrect data_field type
    def test_tweetdb_create_object_3(self):
        self.db_action.not_print_raw()
        data_field = 0
        data_list = [1,2]

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == 'Failed to create object'

    #correct field_list but incorrect data_list
    def test_tweetdb_create_object_4(self):
        self.db_action.not_print_raw()
        data_field = ['test1','test2']
        data_list = 0

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        print(test_object)
        assert test_object == 'Failed to create object'
    
    #incorrect field_list and data_list
    def test_tweetdb_create_object_5(self):
        self.db_action.not_print_raw()
        data_field = 0
        data_list = 1

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == 'Failed to create object'
    
    #field_list and data_list members not match

    #data_field < data_list
    def test_tweetdb_create_object_6(self):
        self.db_action.not_print_raw()
        data_field = ['test1','test2']
        data_list = [1,2,3]

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == 'Amount of key and value not match'

    #data_field > data_list
    def test_tweetdb_create_object_7(self):
        self.db_action.not_print_raw()
        data_field = ['test1','test2','test3']
        data_list = [1,2]

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == 'Amount of key and value not match'

if __name__ == '__main__':
    unittest.main()