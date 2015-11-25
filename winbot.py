try:
    import json
except ImportError:
    import simplejson as json

import tweepy, sys
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

##########################################################
############## Tweepy Streamer ##############
##########################################################
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
##########################################################


##########################################################
############## Create retweet API call from tweet_id ###
##########################################################
def retweet_url(tweet_id):
    return ("https://api.twitter.com/1.1/statuses/retweet/" 
           + tweet_id + ".json")
##########################################################


############## Follows a user if a competition tweet requires it
def follow_user(tweet):
    tweet_str = tweet['text'].lower()
    follow_strs = ["follow", "follows", "Follow", "follows", "foll", 
            "flw", "follo", "F &", "F&", "& F", "&F"]
    if any(x in tweet_str for x in follow_strs):
        user_id = tweet['user']['id']
        screen_name = tweet['user']['screen_name']
        api.create_friendship(user_id)
        print('Created friendship with user ' + screen_name)
##########################################################


##########################################################
############## Strip 'copied' tweets to searchable remnants (very hacky right now...)
##########################################################
# TODO keep beginning 'section' after 'RT' to determine user
# note: maybe not, as some 'copied' retweets don't necessarily follow this structure.
#       perhaps safer to keep current approach of simply searching on remaining string
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
##########################################################


##########################################################
############## Favorites a tweet if a competition tweet requires it
##########################################################
def favorite_tweet(tweet):
    tweet_str = tweet['text']
    fav_strs = ["favorite", "like", "fave", "fav", "fvrt", "fvrite"]
    if any(x in tweet_str for x in fav_strs):
        tweet_id = tweet['id_str']
        api.create_favorite(tweet_id)
##########################################################


##########################################################
############## Perform a retweet given a tweet
##########################################################
def retweet(tweet):

    # Skip unwanted tweets
    unwanted = ['MTV', 'Bieber'];
    if any(x in tweet['text'] for x in unwanted):
        return

    # Retweet
    try:
        api.retweet(tweet['id'])

        # Show Tweet re-tweeted only if re-tweeted successfully
        print ('tweet id:   ' + json.dumps(tweet['id']))
        print ('user name:  ' + json.dumps(tweet['user']['screen_name']))
        print ('tweet text: ' + json.dumps(tweet['text']))
        print ('fav count:  ' + json.dumps(tweet['favorite_count']))
    
        # Follow a user for a competition if needed
        follow_user(tweet)

        # Like a tweet for a competition if needed
        favorite_tweet(tweet)

        # Line gap between retweets
        print ()

    except tweepy.error.TweepError as e:
        pass
##########################################################

if __name__ == "__main__":

    ### User-specific details ###
    ACCESS_TOKEN= '34480377-tdxPPEkuHXN9dXJT1xXS7vaLymRzQZ9mCa4PXINrS'
    ACCESS_SECRET= 'ZfTnmi7fydT7LIUSbsob0e6f4LKrPp5QLdlRyIiFwLyHp'
    CONSUMER_KEY = 'tPOa8XtMxtf7wbaAvHu1icj78'
    CONSUMER_SECRET= 'pl6aM41c4gT41Jo0B1EWZLFPuNTuRFlxex6yUaGEAAFxL3TAap'
    
    ### Tweepy authentication
    auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    # TODO aim to remove and use tweepy library
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

    ##########################################################
    ############### Iterate through all tweets ###############
    ##########################################################
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
    
            # Create search filter for copied tweets
            try:
                secondary_tweets = twitter.search.tweets(q=new_tweet_str, lang='en', count=30, retweeted=False)['statuses']
            except:
                print ('Rate limit exceeded due to allowed searches within ~15 minute time frame. Please try again later.')
                sys.exit(0)
    
            # Go through each secondary tweet
            for s_tweet in secondary_tweets:
                if 'id_str' not in s_tweet:
                    continue
                if s_tweet["favorite_count"] > 2:
                    retweet(s_tweet)
            continue

        # Directly retweet original competition tweets
        else:
            ### Retweet competition tweet ###
            retweet(tweet)
    ##########################################################
    
    print (str(retweet_success) + ' retweet successes.')
    print (str(retweet_fail) + ' retweet fails.')
    print (len(tweets))
