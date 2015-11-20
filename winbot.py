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

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

def retweet_url(tweet_id):
    return "https://api.twitter.com/1.1/statuses/retweet/" + tweet_id + ".json"

ACCESS_TOKEN= '34480377-tdxPPEkuHXN9dXJT1xXS7vaLymRzQZ9mCa4PXINrS'
ACCESS_SECRET= 'ZfTnmi7fydT7LIUSbsob0e6f4LKrPp5QLdlRyIiFwLyHp'
CONSUMER_KEY = 'raKeRc7dfqPdVydVtahlGOmrQ'
CONSUMER_SECRET= '4eFVlM5sBG9KY90Z7WQujiteaFIO4LBTzKvIYjl4ES0ccmqNkd'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = TwitterStream(auth=oauth)

iterator = twitter_stream.statuses.filter(track="RT win", language="en", retweeted="false")

tweet_count = 5
for tweet in iterator:
    tweet_count -= 1
    print (json.dumps(tweet['id_str']))
    print (json.dumps(tweet['text']))
    print ()
    if tweet_count <= 0:
        break
