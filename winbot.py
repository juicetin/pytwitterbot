# import urllib
# import oauth2 
# 
# CONSUMER_KEY = 'raKeRc7dfqPdVydVtahlGOmrQ'
# CONSUMER_SECRET= '4eFVlM5sBG9KY90Z7WQujiteaFIO4LBTzKvIYjl4ES0ccmqNkd'
# 
# def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
#     consumer = oauth2.Consumer(key=CONSUMER_KEY,secret=CONSUMER_SECRET)
#     token = oauth2.Token(key=key, secret=secret)
#     client = oauth2.Client(consumer, token)
#     resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
#     return content
# 
# home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/home_timeline.json', CONSUMER_KEY, CONSUMER_SECRET)

try:
    import json
except ImportError:
    import simplejson as json

import tweepy
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

### Create retweet API call from tweet_id ###
def retweet_url(tweet_id):
    return "https://api.twitter.com/1.1/statuses/retweet/" + tweet_id + ".json"

### User-specific details ###
ACCESS_TOKEN= '34480377-tdxPPEkuHXN9dXJT1xXS7vaLymRzQZ9mCa4PXINrS'
ACCESS_SECRET= 'ZfTnmi7fydT7LIUSbsob0e6f4LKrPp5QLdlRyIiFwLyHp'
CONSUMER_KEY = 'tPOa8XtMxtf7wbaAvHu1icj78'
CONSUMER_SECRET= 'pl6aM41c4gT41Jo0B1EWZLFPuNTuRFlxex6yUaGEAAFxL3TAap'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

twitter_stream = TwitterStream(auth=oauth)

### Create iterator for all 
iterator = twitter_stream.statuses.filter(track="RT win", language="en", retweeted="false")

tweet_count = 2500
retweet_fail = 0
retweet_success = 0

### Iterate through all tweets meeting search conditions ###
for tweet in iterator:
    tweet_count -= 1
    tweet_id = str(tweet['id']) # this sometimes seems to throw an error tweet['id_str']
    tweet_str = tweet['text']

    ### Retweet competition tweet ###
    try:
        # TODO figure out a way to see that people don't have 'retweets' that aren't classed
        # as 'retweets', perhaps by identifying usernames in tweets and checking that
        # against the user screen_name

        api.retweet(tweet_id)
        retweet_success += 1

        # Show Tweet re-tweeted only if re-tweeted successfully
        print (json.dumps(tweet_id))
        print (json.dumps(tweet_str))
        print ()

        # Follow a user for a competition if needed
        tweet_str = tweet_str.lower()
        if 'follow' in tweet_str or 'follows' in tweet_str:
            user_id = tweet['user']['id']
            screen_name = tweet['user']['screen_name']
            api.create_friendship(user_id)
            print('Created friendship with user ' + screen_name)

    except tweepy.error.TweepError as e:
        retweet_fail += 1

    if tweet_count <= 0:
        break

print (str(retweet_success) + 'retweet successes.')
print (str(retweet_fail) + ' retweet fails.')
