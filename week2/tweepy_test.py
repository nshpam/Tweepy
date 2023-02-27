# coding=utf8
import tweepy
import config

auth = tweepy.OAuth1UserHandler(
      config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
      )
api = tweepy.API(auth)

trends = api.get_place_trends(config.WOEid)

print(trends[0])

# print(trends.keys())

# trends_list = trends[0]['trends'][:config.ranking_top]

# for trend in trends_list:
#     print(trend['name'])