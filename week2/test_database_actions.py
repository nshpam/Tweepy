import unittest
from unittest.mock import patch, MagicMock
import database_action
from  collections import namedtuple

class FakeMongoDB():

    def pymongo_MongoClient(self, collections=[]):
        mock_client = MagicMock()

        if collections == []:
            return mock_client

        temp_list = []
        for col in collections:
            temp_list.append(col)

        mock_client.list_collection_names.return_value = temp_list
        return mock_client
    
    def Mongo_collection(self, num, mock_value):
        
        mock_col = MagicMock()
        mock_col.name = 'mock_col'+str(num)
        mock_col.find.return_value = mock_value

        return mock_col
    


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

    #test tweetdb_showall_collection

    #correct collection
    def test_tweetdb_showall_collection_1(self):
        
        mock_client = FakeMongoDB().pymongo_MongoClient(['mock_col1', 'mock_col2', 'mock_col3', 'mock_col4'])

        mock_col1 = FakeMongoDB().Mongo_collection(1, [{'a1':'ant', 'a2':'app'}])
        mock_col2 = FakeMongoDB().Mongo_collection(2, [{'b1':'bat', 'b2':'boy'}])
        mock_col3 = FakeMongoDB().Mongo_collection(3, [{'c1':'cat', 'c2':'cap'}])
        mock_col4 = FakeMongoDB().Mongo_collection(4, [{'d1':'dog', 'd2':'dose'}])

        self.db_action.mydb = mock_client
        
        collection_list = [mock_col1, mock_col2, mock_col3, mock_col4]
        
        result = self.db_action.tweetdb_showall_collection(collection_list)
        assert result == {'mock_col1':[{'a1':'ant', 'a2':'app'}], 
                          'mock_col2':[{'b1':'bat', 'b2':'boy'}],
                          'mock_col3':[{'c1':'cat', 'c2':'cap'}],
                          'mock_col4':[{'d1':'dog', 'd2':'dose'}]}

    #incorrect collection
    
    #incorrect collection in collection list
    def test_tweetdb_showall_collection_2(self):
        
        mock_client = MagicMock()

        mock_client.list_collection_names.return_value = ['mock_col1', 'mock_col2', 'mock_col3', 'mock_col4']

        self.db_action.myclient = mock_client
        self.db_action.mydb = self.db_action.myclient[self.mongo_db]
        
        collection_list = (1,2,3,4)
        
        result = self.db_action.tweetdb_showall_collection(collection_list)
        assert result == 'Invalid Collection List'
    
    #incorrect collection list
    #incorrect collection in collection list
    def test_tweetdb_showall_collection_3(self):
        
        mock_client = MagicMock()

        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = 0

        mock_col1.name = 'mock_col1'
        mock_col2.name = 'mock_col2'
        mock_col3.name = 'mock_col3'

        mock_col1.find.return_value = [{'a1':'ant', 'a2':'app'}]
        mock_col2.find.return_value = [{'b1':'bat', 'b2':'boy'}]
        mock_col3.find.return_value = [{'c1':'cat', 'c2':'cap'}]

        mock_client.list_collection_names.return_value = ['mock_col1', 'mock_col2', 'mock_col3', 'mock_col4']

        self.db_action.myclient = mock_client
        self.db_action.mydb = self.db_action.myclient[self.mongo_db]
        
        collection_list = [
            mock_col1,
            mock_col2,
            mock_col3,
            mock_col4
        ]
        
        result = self.db_action.tweetdb_showall_collection(collection_list)
        assert result == 'Invalid Collection'
    
    #test tweetdb_show_collection
    def test_tweetdb_show_collection_1(self):

        mock_client = MagicMock()

        mock_col1 = MagicMock()
        mock_col1.name = 'mock_col1'
        mock_col1.find.return_value = [{'id':'09234', 'sentiment':'positive'}, 
                                       {'id':'09235', 'sentiment':'positive'},
                                       {'id':'09236', 'sentiment':'negative'}]
        self.db_action.myclient = mock_client
        self.db_action.mydb = self.db_action.myclient[self.mongo_db]

        data_field = ['sentiment']
        data_list = ['positive']

        fake_object = self.db_action.tweetdb_create_object(data_field, data_list)

        result = self.db_action.tweetdb_show_collection(mock_col1.name, mock_col1, fake_object)
        # print('here',result)

if __name__ == '__main__':
    unittest.main()