#!/usr/bin/env python3

try:
    import json
except ImportError:
    import simplejson as json

import tweepy, sys, urllib
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

### User-specific details ###
ACCESS_TOKEN= '34480377-tdxPPEkuHXN9dXJT1xXS7vaLymRzQZ9mCa4PXINrS'
ACCESS_SECRET= 'ZfTnmi7fydT7LIUSbsob0e6f4LKrPp5QLdlRyIiFwLyHp'
CONSUMER_KEY = 'tPOa8XtMxtf7wbaAvHu1icj78'
CONSUMER_SECRET= 'pl6aM41c4gT41Jo0B1EWZLFPuNTuRFlxex6yUaGEAAFxL3TAap'

# Globals
following_file_path = '/home/pi/twitter_competition_bot/following.txt'
following_list = []
following_file_opened = False
retweets_file_path = '/home/pi/twitter_competition_bot/retweets.txt'
unwanted_keywords = ['MTV', 'Bieber', 'fuck', 'pussy', 'if you think', 'help me win'];
fav_strs = ["favorite", "like", "fave", "fav", "fvrt", "fvrite", "LK ", " LK"]

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

##########################################################
############## Create a list of followed users
##########################################################
#TODO
##########################################################


############## Follows a user if a competition tweet requires it
def follow_user(tweet):
    tweet_str = tweet['text'].lower()
    follow_strs = ["follow", "follows", "Follow", "follows", "foll", 
            "flw", "follo", "F &", "F&", "& F", "&F"]
    if any(x in tweet_str for x in follow_strs):

        #TODO Check whether (my defined) follow limit is reached -
        # if so, unfollow oldest 'friend' before following a new user

        # Follow a user
        user_id = tweet['user']['id']
        screen_name = tweet['user']['screen_name']
        api.create_friendship(user_id)
        print('Created friendship with user ' + screen_name)
        with open(following_file_path, 'a') as f: f.write(screen_name + '\n')
##########################################################


##########################################################
############## Strip 'copied' tweets to searchable remnants (very hacky right now...)
##########################################################
# TODO keep beginning 'section' after 'RT' to determine user
# note: maybe not, as some 'copied' retweets don't necessarily follow this structure.
#       perhaps safer to keep current approach of simply searching on remaining string
def strip_copied_tweets(tweet_text):
    while (tweet_text.startswith("RT")):
        colon_index = tweet_text.find(':')
        if colon_index == -1:
            colon_index = 0
        tweet_text = tweet_text[colon_index+2:]
        tweet_text_parts = tweet_text.split("http")
        tweet_text = tweet_text_parts[0]

    return tweet_text
##########################################################


##########################################################
############## Favorites a tweet if a competition tweet requires it
##########################################################
def favorite_tweet(tweet):
    tweet_str = tweet['text']
    tweet_str = tweet_str.lower()
    if any(x in tweet_str for x in fav_strs):
        tweet_id = tweet['id_str']
        api.create_favorite(tweet_id)
        print ('Tweet liked.')
##########################################################


##########################################################
############## Prints some basic tweet info
##########################################################
def print_tweet_info(tweet):
    # Show Tweet re-tweeted only if re-tweeted successfully
    print ('tweet id:   ' + json.dumps(tweet['id']))
    print ('user name:  ' + json.dumps(tweet['user']['screen_name']))
    print ('tweet text: ' + json.dumps(tweet['text']))
    print ('fav count:  ' + json.dumps(tweet['favorite_count']))
    print ('retweets:   ' + json.dumps(tweet['retweet_count']))


##########################################################
############## Perform a retweet given a tweet
##########################################################
def retweet(tweet):

    # Skip unwanted tweets
    if any(x in tweet['text'] for x in unwanted_keywords):
        return

    # Retweet
    try:
        # Retweet and print tweet to file, as well as basic info to console
        api.retweet(tweet['id'])
        with open(retweets_file_path, 'a') as f: f.write(tweet['text'] + '\n')
        print_tweet_info(tweet)
    
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
    
    ### Tweepy authentication
    auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth_handler=auth)
    
    # TODO aim to remove and use tweepy library
    ### Twitter (library) authentication
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_stream = TwitterStream(auth=oauth)
    twitter = Twitter(auth=oauth)
    
    ### Tweepy iterators
    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    # myStream.filter(track=['RT'], async=True)
    
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
        
        # Skip broken JSON objects
        if 'id_str' in tweet:
            tweet_id = tweet['id_str'] # this sometimes seems to throw an error tweet['id_str']
        else:
            continue

        tweet_str = tweet['text']

        # Skip unwanted tweets
        if any(x in tweet_str for x in unwanted_keywords):
            continue

        # TODO a 'document' search here where the 300 (to tune?) most recent tweets are stored in a keyword document
        # matrix, and if the tweet being searched is more than ~80% similar (TODO tune!!) then skip/don't waste a search
                                      ########################################################
    
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
            success_tweets = 0
            for s_tweet in secondary_tweets:
                if 'id_str' not in s_tweet:
                    continue
                if s_tweet["favorite_count"] > 2:
                    retweet(s_tweet)

            # NOTE - unreliable method - 'bad' tweets include good ones I've already retweeted and hence fail.
            # # Log bad tweets, TODO find patterns to exclude these in future
            # if success_tweets == 0 :
            #     with open('rejected_tweets.txt', 'a') as f: f.write(tweet_str + '\n')
            #     #print (tweet)
            continue

        # Directly retweet original competition tweets
        else:
            ### Retweet competition tweet ###
            retweet(tweet)
    ##########################################################
