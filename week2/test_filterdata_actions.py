import unittest
from twitterDataProcessing import FilterData

class TestFilterData(unittest.TestCase):
    def setUp(self):
        self.filter_data = FilterData()
        
    # Test Filter url function
    def test_FilterUrl(self):
        # Test with URL starting with https://
        self.assertTrue(self.filter_data.FilterUrl("https://example.com"))
        # Test with URL not starting with https://
        self.assertFalse(self.filter_data.FilterUrl("http://example.com"))
        self.assertFalse(self.filter_data.FilterUrl("ftp://ftp.example.com/file.txt"))
        # Test with URL not containing any protocol
        self.assertFalse(self.filter_data.FilterUrl("example.com"))
        # Test with empty string
        self.assertFalse(self.filter_data.FilterUrl(""))
        
    # Test Filter number function
    def test_filter_num(self):
        input_text = "I have 3 apples and 2 bananas"
        expected_output = "I have  apples and  bananas"

        output = self.filter_data.FilterNum(input_text)

        self.assertEqual(output, expected_output)
        
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
    
    # Test Filters function
    def test_filters(self):
        raw_list = '◡̈'
        expected_output = ''
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)
        
        raw_list = 'ก'
        expected_output = 'ก'
        self.assertEqual(self.filter_data.Filters(raw_list), expected_output)
    
if __name__ == '__main__':
    unittest.main()