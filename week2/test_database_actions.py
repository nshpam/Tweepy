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

    #test if function were called with the specific arguments
    @patch('pymongo.MongoClient')
    def test_connect_MongoClient(self, mock_client):
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
        mock_client.assert_called_with(self.mongo_client) #first argument
        mock_client().__getitem__.assert_called_with(self.mongo_db) #second argument
        mock_client().__getitem__().__getitem__.assert_called_with(self.mongo_col) #third argument
    
    #test if connect to the correct database
    def test_tweetdb_object(self):
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
        assert self.db_action.mydb.name == self.mongo_db
        assert self.db_action.mydb.list_collection_names() == self.mongo_all_col
    
    #test if connect to the correct collection
    def test_connect_MongoCol(self):
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)
        assert self.db_action.mycol.name == self.mongo_col

    #test if not_print_raw was called in tweetdb_object
    def test_not_print_raw_tweetdb_object(self):

        mock = MagicMock()
        self.db_action.not_print_raw = mock

        self.db_action.not_print_raw()
        self.db_action.tweetdb_object(self.mongo_client, self.mongo_db, self.mongo_col)

        mock.assert_called_once()
    
    #test if tweetdb_create_object can create the correct object
    def test_tweetdb_create_object(self):
        data_field = ['test1','test2']
        data_list = [1,2]
        expect_object = {'test1':1, 'test2':2}

        test_object = self.db_action.tweetdb_create_object(data_field, data_list)
        assert test_object == expect_object

if __name__ == '__main__':
    unittest.main()