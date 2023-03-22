import unittest
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, '../')
import Transform

class TestFilterData(unittest.TestCase):
    def setUp(self):
        self.filter_data = Transform.FilterData()
  
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

        raw_list = 'This is some ◡̈ Text with {กก braces} and กำหนด หัวข้อ รายละเอียด https://example.com #เทส'
        expected_output = 'this is some text with {กก braces} and กำหนด หัวข้อ รายละเอียด'
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)
        
        raw_list = []
        expected_output = 'Invalid data type'
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)

if __name__ == '__main__':
    unittest.main()