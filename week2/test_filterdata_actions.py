import unittest
from twitterDataProcessing import FilterData, ConnectLextoPlus
from unittest.mock import patch, MagicMock
class TestConnectLextoPlus(unittest.TestCase):
    def setUp(self):
        self.connect_api = ConnectLextoPlus()
        self.api_key = '1234'
        self.url = 'https://example.com/api'
        
        
    def get_mock_response(self, api_key, url_to_send, data_dict):
        with patch.object(ConnectLextoPlus, 'ConnectApi') as mock_method:
            mock_connected = MagicMock()
            mock_connected.status_code = 200
            mock_connected.text = 'This API method connects correctly.'
            mock_method.return_value = mock_connected

            response = self.connect_api.ConnectApi(api_key, url_to_send, data_dict)

            mock_method.assert_called_once_with(api_key, url_to_send, data_dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, 'This API method connects correctly.')


    @patch('requests.get')
    def test_connect_api_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'Mock response'
        mock_get.return_value = mock_response

        data = {'input': 'ข้อความที่ต้องการตัดคำ'}
        response = self.connect_api.ConnectApi(self.api_key, self.url, data)

        mock_get.assert_called_once_with(self.url, params=data, headers={'Apikey': self.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Mock response')

    @patch('requests.get')
    def test_connect_api_failure(self, mock_get):
        mock_get.return_value.status_code = 404

        data = {'input': 'ข้อความที่ต้องการตัดคำ'}
        response = self.connect_api.ConnectApi(self.api_key, self.url, data)

        mock_get.assert_called_once_with(self.url, params=data, headers={'Apikey': self.api_key})
        self.assertEqual(response.status_code, 404)

class TestFilterData(unittest.TestCase):
    def setUp(self):
        self.filter_data = FilterData()
  
    # Test Filter url function
    def test_FilterUrl(self):
        # Test with URL starting with https://
        self.assertTrue(self.filter_data.FilterUrl("https://example.com"))
        # Test with URL not starting with https://
        self.assertTrue(self.filter_data.FilterUrl("http://example.com"))
        # Test with URL not containing any protocol
        self.assertFalse(self.filter_data.FilterUrl("example.com"))
        # Test with empty string
        self.assertFalse(self.filter_data.FilterUrl(""))
        # Test Invalid data type
        self.assertFalse(self.filter_data.FilterUrl([]))
        
    # Test Filter number function
    def test_filter_num(self):
        raw_text = "I have 3 apples and 2 bananas"
        expected_output = "I have  apples and  bananas"
        self.assertEqual(self.filter_data.FilterNum(raw_text), expected_output)

        raw_text = []
        expected_output = 'Invalid data type'
        self.assertEqual(self.filter_data.FilterNum(raw_text), expected_output)
        
    # Test Filter Special Char function
    def test_filter_special_char(self):
        raw_text = "This is ◡̈ some text that we want to process"
        expected_output = "this is some text that we want to process"
        self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)

        raw_text = "Thai {curly braces} with some special characters"
        expected_output = "thai {curly braces} with some special characters"
        self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)
        
        raw_text = "This is some ◡̈ Text with {กก braces} and THAI กำหนด หัวข้อ รายละเอียด"
        expected_output = "this is some text with {กก braces} and thai กำหนด หัวข้อ รายละเอียด"
        self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)
        
        raw_text = "This is some ◡̈ Text with {กก braces} and กำหนด หัวข้อ รายละเอียด"
        expected_output = "this is some text with {กก braces} and กำหนด หัวข้อ รายละเอียด"
        self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)

        raw_text = []
        expected_output = 'Invalid data type'
        self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)
    
    # Test Filters function
    def test_filters(self):
        raw_list = '◡̈'
        expected_output = ''
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)
        
        raw_list = 'ก@'
        expected_output = 'ก'
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)

        raw_list = 'This is some ◡̈ Text with {กก braces} and กำหนด หัวข้อ รายละเอียด https://example.com'
        expected_output = 'this is some text with {กก braces} and กำหนด หัวข้อ รายละเอียด'
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)
        
        raw_list = []
        expected_output = 'Invalid data type'
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)

if __name__ == '__main__':
    unittest.main()