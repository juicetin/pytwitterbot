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
    follow_strs = ["follow", "follows", "Follow", "follows", "foll", "flw", "follo"]
    if any(x in tweet_str for x in follow_strs):
        user_id = tweet['user']['id']
        screen_name = tweet['user']['screen_name']
        api.create_friendship(user_id)
        print('Created friendship with user ' + screen_name)

### Strip 'copied' tweets to searchable remnants (very hacky right now...)
def strip_copied_tweets(tweet_text):
    colon_index = tweet_text.find(':')
    tweet_text = tweet_text[colon_index+2:]
    if '&amp;' in tweet_text:
        rt_index = tweet_text.find('RT &amp;')
        tweet_text = tweet_text[rt_index+8:]
    tweet_text_words = tweet_text.split(' ')
    if len(tweet_text_words) >= 11:
        tweet_text_words = tweet_text_words[1:10]
    tweet_text = ' '.join(tweet_text_words)
    return tweet_text

### Perform a retweet given a tweet
def retweet(tweet):
    try:
        api.retweet(tweet['id'])

        # Show Tweet re-tweeted only if re-tweeted successfully
        print (json.dumps(tweet['id']))
        print (json.dumps(tweet['text']))
        print (json.dumps(tweet['favorite_count']))
        print ()
    
        # Follow a user for a competition if needed
        follow_user(tweet['text'])
    except tweepy.error.TweepError as e:
        pass

### Tweepy Streamer
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


### Iterate through all tweets meeting search conditions ###
# TODO remove by switching to tweepy
filter_string = "RT win"

# Choose whether to stream or search for tweets
if (len(sys.argv) > 1 and sys.argv[1] == 'search'):
    tweets = twitter.search.tweets(q=filter_string, lang='en', count=101, retweeted=False)['statuses']
else:
    tweets = twitter_stream.statuses.filter(track=filter_string, language="en", retweeted="false")
    
# Iterate through all tweets
for tweet in tweets:
    tweet_count -= 1

    # Skip broken JSON objects
    if 'id_str' in tweet:
        tweet_id = tweet['id_str'] # this sometimes seems to throw an error tweet['id_str']
    else:
        continue
    tweet_str = tweet['text']


    # Filter out 'copied' 'retweets'
    if tweet["favorite_count"] < 2:

        # Strip 'copied' tweet down to a bare minimum (extremely rough here. Chance for some regex :muscle:)
        new_tweet_str = strip_copied_tweets(tweet_str)

        # Search filter
        secondary_tweets = twitter.search.tweets(q=new_tweet_str, lang='en', count=101, retweeted=False)['statuses']

        for s_tweet in secondary_tweets:
            if 'id_str' not in s_tweet:
                continue
            if s_tweet["favorite_count"] > 1:
                retweet(s_tweet)
        continue

    ### Retweet competition tweet ###
    retweet(tweet)

print (str(retweet_success) + ' retweet successes.')
print (str(retweet_fail) + ' retweet fails.')
print (len(tweets))
