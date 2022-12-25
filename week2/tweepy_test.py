import tweepy
import config

#connect to twitter
auth = tweepy.OAuth1UserHandler(
   config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
)
api = tweepy.API(auth)
# print(api)
try:
   user = api.get_user(screen_name='pammy113357') #@...
except Exception as e:
   print(e)
# print(user.screen_name)

# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# public_tweets = api.user_timeline(screen_name='iconnnz')
# for tweet in public_tweets:
#     print(tweet.text)