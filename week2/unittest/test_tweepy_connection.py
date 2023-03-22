import unittest
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, '../')
import config
import Extract
import tweepy
import datetime

class TweepyConnectionTest(unittest.TestCase):

    @patch('tweepy.OAuth1UserHandler')
    def test_OAuth1UserHandler(self, mock_client):
        
        #mock tweepy config data
        mock_config = MagicMock()
        mock_config.consumer_key = config.consumer_key
        mock_config.consumer_secret = config.consumer_secret
        mock_config.access_token = config.access_token
        mock_config.access_token_secret = config.access_token_secret

        Extract.ExtractTwitter().ConnectTweepy()

        mock_client.assert_called_once_with(
            mock_config.consumer_key, 
            mock_config.consumer_secret, 
            mock_config.access_token, 
            mock_config.access_token_secret)
        
    def test_search_twitter(self):
        keyword = '#รีวิวหนัง'

        #test correct search type
        settings = {
        'search_type' : config.search_type,
        'num_tweet' : 1,
        'start_d' : datetime.date(2023, 3, 15),
        'end_d': datetime.date(2023, 3, 20),
        'mode' : 'keyword'
        }
        tweet_list = Extract.ExtractTwitter().SearchTwitter(keyword, settings)

        assert tweet_list != []
        assert len(tweet_list) == 1

        #invalid keyword
        keyword_1 = 0

        tweet_list = Extract.ExtractTwitter().SearchTwitter(keyword_1, settings)
        assert tweet_list == 'Invalid keyword'

        #invalid settings
        settings_1 = []
        tweet_list = Extract.ExtractTwitter().SearchTwitter(keyword, settings_1)
        assert tweet_list == 'Invalid settings'

        # invalid search_type
        settings_1 = {
        'search_type' : 'a',
        'num_tweet' : 1,
        'start_d' : datetime.date(2023, 3, 15),
        'end_d': datetime.date(2023, 3, 20),
        'mode' : 'keyword'
        }

        tweet_list = Extract.ExtractTwitter().SearchTwitter(keyword, settings_1)
        assert tweet_list == 'Invalid search_type'

        #invalid num_tweet
        settings_1 = {
        'search_type' : config.search_type,
        'num_tweet' : 'a',
        'start_d' : datetime.date(2023, 3, 15),
        'end_d': datetime.date(2023, 3, 20),
        'mode' : 'keyword'
        }

        tweet_list = Extract.ExtractTwitter().SearchTwitter(keyword, settings_1)
        assert tweet_list == 'Invalid num_tweet'

    def test_pull_trends(self):
        extract = Extract.ExtractTwitter()
        api = extract.ConnectTweepy()
        trends_dict = extract.PullTrends(api, config.WOEid)
        
        assert trends_dict['hashtags'] != []
        assert len(trends_dict['hashtags']) == 10

        assert trends_dict['words'] != []
        assert len(trends_dict['words']) == 10

        #test invalid api
        trends_dict = extract.PullTrends(None, config.WOEid)
        assert trends_dict == 'Cannot connect to tweepy API please try again.'

        #test invalid woeid
        trends_dict = extract.PullTrends(api, 'a')
        assert trends_dict == 'Invalid woeid'



if __name__ == '__main__':
    unittest.main()
        