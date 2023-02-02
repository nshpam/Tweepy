import tweepy
import config

# Authenticate to Twitter API
auth = tweepy.OAuth1UserHandler(config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret)
api = tweepy.API(auth)

# Check if the user exists
try:
    user = api.get_user(screen_name='@tw94sh')
    # Get the latest tweet from the user
    tweet = api.user_timeline(screen_name='@tw94sh', count=1)[0]

    # Check if the tweet has a place
    if tweet.place:
        # Print the location of the tweet
        print(tweet.place.full_name)
    else:
        print("No location information available.")
except tweepy.TweepError as error:
    if error.api_code == 34:
        print("User does not exist.")
    else:
        print(error)