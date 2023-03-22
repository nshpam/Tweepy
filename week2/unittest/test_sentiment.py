import unittest
from unittest.mock import patch
import sys
import datetime

sys.path.insert(0, '../')
import Sentiment

class SentimentTest(unittest.TestCase):
    def test_covert_polar(self):
        sentiment = Sentiment.SentimentAnalysis()
        #input positive
        polar = sentiment.ConvertPolar('positive')
        assert polar == 1
        #input negative
        polar = sentiment.ConvertPolar('negative')
        assert polar == -1
        #input neutral
        polar = sentiment.ConvertPolar('')
        assert polar == 0
        #input invalid polar
        polar = sentiment.ConvertPolar([])
        assert polar == 'Invalid polar'
    
    def test_sentiment_perform(self):
        sentiment = Sentiment.SentimentAnalysis()
        #valid perform
        sentiment_dict = sentiment.Perform('#iphone')

        assert sentiment_dict != {}

        for id in sentiment_dict:
            assert list(sentiment_dict[id].keys()) == ['id','keyword','date','input','score','polar']
        

if __name__ == '__main__':
    unittest.main()