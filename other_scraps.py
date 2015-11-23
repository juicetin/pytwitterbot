## TODO figure out a way to see that people don't have 'retweets' that aren't classed
## as 'retweets', perhaps by identifying usernames in tweets and checking that
## against the user screen_name
## check https://dev.twitter.com/overview/api/tweets

#if "quoted_status_str" in tweet:
#    print (json.dumps(tweet['quoted_status']))

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


#try
#    retweet_should_succeeds += 1
#    api.retweet(tweet_id)
#    retweet_success += 1

#    # Show Tweet re-tweeted only if re-tweeted successfully
#    print (json.dumps(tweet_id))
#    print (json.dumps(tweet_str))
#    print (json.dumps(tweet['favorite_count']))
#    print ()

#    # Follow a user for a competition if needed
#    follow_user(tweet_str)

#except tweepy.error.TweepError as e:
#    retweet_fail += 1

#if tweet_count <= 0:
#    break

