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
    # Test Filter Special Char
    # def test_filter_special_char(self):
        # raw_text = "This is 🅕🅐🅝🅒 special characters"
        # expected_output = "This is  special characters"
        # self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)

        # raw_text = "Thai {text} with some special characters"
        # expected_output = "thai text with some special characters"
        # self.assertEqual(self.filter_data.FilterSpecialChar(raw_text), expected_output)
        
    
if __name__ == '__main__':
    unittest.main()