try:
    import json
except ImportError:
    import simplejson as json

import tweepy, sys
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

### Create retweet API call from tweet_id ###
def retweet_url(tweet_id):
    return "https://api.twitter.com/1.1/statuses/retweet/" + tweet_id + ".json"

### Follows a user if a competition tweet requires it
def follow_user(tweet_str):
    tweet_str = tweet_str.lower()
    follow_strs = ["follow", "follows", "Follow", "follows"]
    if any(x in tweet_str for x in follow_strs):
        user_id = tweet['user']['id']
        screen_name = tweet['user']['screen_name']
        api.create_friendship(user_id)
        print('Created friendship with user ' + screen_name)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

### User-specific details ###
ACCESS_TOKEN= '34480377-tdxPPEkuHXN9dXJT1xXS7vaLymRzQZ9mCa4PXINrS'
ACCESS_SECRET= 'ZfTnmi7fydT7LIUSbsob0e6f4LKrPp5QLdlRyIiFwLyHp'
CONSUMER_KEY = 'tPOa8XtMxtf7wbaAvHu1icj78'
CONSUMER_SECRET= 'pl6aM41c4gT41Jo0B1EWZLFPuNTuRFlxex6yUaGEAAFxL3TAap'

### Tweepy authentication
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# TODO remove
### Twitter (library) authentication
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
twitter = Twitter(auth=oauth)

### Tweepy iterators
# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
# myStream.filter(track=['RT'], async=True)

# Counter initialisation
tweet_count = 2500
retweet_fail = 0
retweet_success = 0
retweet_should_succeeds = 0

# for tweet in search_iterator['statuses']:
#     if (tweet['favorite_count'] > 1):
#         print (tweet['id_str'])
#         print (tweet['text'])

### Iterate through all tweets meeting search conditions ###
# TODO remove by switching to tweepy
### Create iterator for all retweet-to-win competition tweets
filter_string = "RT Win,win,WIN -:"
if (len(sys.argv) > 1 and sys.argv[1] == 'search'):
    tweets = twitter.search.tweets(q=filter_string, lang='en', count=100000000000, retweeted=False)['statuses']
else:
    tweets = twitter_stream.statuses.filter(track=filter_string, language="en", retweeted="false")
    
for tweet in tweets:
#for tweet in search_iterator['statuses']:
    tweet_count -= 1
    if 'id_str' in tweet:
        tweet_id = str(tweet['id_str']) # this sometimes seems to throw an error tweet['id_str']
    else:
        continue
    tweet_str = tweet['text']

    # TODO figure out a way to see that people don't have 'retweets' that aren't classed
    # as 'retweets', perhaps by identifying usernames in tweets and checking that
    # against the user screen_name
    # check https://dev.twitter.com/overview/api/tweets

    if "quoted_status_str" in tweet:
        print (json.dumps(tweet['quoted_status']))

    ### Hacky prevention of individual user retweets
    #   (as opposed to actual competition RT tweets)
    #   try doing a search on the original tweet being re-tweeted
    #   and retweet that

    # Print info
    print (json.dumps(tweet_id))
    print (json.dumps(tweet_str))
    print (json.dumps(tweet['favorite_count']))
    print (json.dumps(tweet['user']['screen_name']))
    print ('Successes so far: ' + str(retweet_success))
    print ('Should succeeds so far: ' + str(retweet_should_succeeds))
    print ()

    if tweet["favorite_count"] < 2:
        continue

    ### Retweet competition tweet ###
    try:
        retweet_should_succeeds += 1
        api.retweet(tweet_id)
        retweet_success += 1

        # Show Tweet re-tweeted only if re-tweeted successfully
        print (json.dumps(tweet_id))
        print (json.dumps(tweet_str))
        print (json.dumps(tweet['favorite_count']))
        print ()

        # Follow a user for a competition if needed
        follow_user(tweet_str)

    except tweepy.error.TweepError as e:
        retweet_fail += 1

    if tweet_count <= 0:
        break

print (str(retweet_success) + ' retweet successes.')
print (str(retweet_fail) + ' retweet fails.')

# if tweet_str.startswith("RT"):
# if ("quoted_status_id_str" in tweet or 
#     "quoted_status" in tweet or 
#     tweet["retweeted"] == True or 
#     "retweeted_status" in tweet or 

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

