import unittest
from unittest.mock import patch, MagicMock
import sys
import config
sys.path.insert(0, '../')

class TweepyConnectionTest(unittest.TestCase):

    @patch('tweepy.OAuth1UserHandler')
    def test_tweepy_connection(self, mock_client):
        
        mock_config = MagicMock()
        mock_config.consumer_key = config.consumer_key
        mock_config.consumer_secret = config.consumer_secret
        mock_config.access_token = config.access_token
        mock_config.access_token_secret = config.access_token_secret

        mock_client.assert_called_with() #first argument

        