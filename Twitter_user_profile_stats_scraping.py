# UTF-8
# Author: Jing Peng
# Last updated: 3/9/2017
# Input: screen name of account
# Output: up to 200 most recent retweets of the account
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import pickle
import codecs
from tweepy.utils import parse_datetime

# Step 1: Authentication
# Go to http://apps.twitter.com and create an app.
# Copy and paste the keys and tokens below
consumer_key="****"
consumer_secret="T***"
access_token="*****"
access_token_secret="****"

# Step 2: Provide Input 
# Provide the screen_name (id) of the Twitter Account you want to scrape
#screen_name = 'rksriram91'
# ****** Ready to Run *********


def get_profile_name():
  profile_name = raw_input("Input a profile name for Influence Score :")
  return profile_name

auth = OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, parser=tweepy.parsers.JSONParser(), retry_count=5)

rate = api.rate_limit_status()
rate_follower_IDs =  rate['resources']['followers']['/followers/ids']['limit'] * 4 # requests per hour
rate_follower_profiles =  rate['resources']['users']['/users/lookup']['limit'] * 4 # requests per hour

# doc explaning each field https://dev.twitter.com/overview/api/tweets
tweet_cols = ['user.id_str', 'user.screen_name','user.description', 'created_at','user.friends_count','user.followers_count','user.favourites_count','user.statuses_count','retweeted_status.id_str',
             'user.location','retweeted_status.retweet_count']

## Print a list of dict variable into csv file
# vals: a list, each element is a dict
# cols: the fields (keys) to be retrieved in each dict
def printList(vals, cols, file_name):
    f = codecs.open(file_name, 'w', 'utf-8')
    f.writelines('\t'.join(cols)+'\n')
    for v in  vals:
        if v==None: continue
        fields = [getDictField(v, e) for  e in  cols]
        f.writelines('\t'.join(fields)+'\n')
    f.close()       

## Access an element in a nested dict variable by key
# d: a dict
# field: the field to be retrieved. seperated by '.' if nested
def getDictField(d, field):
    names = field.split('.')
    for name in  names:
        if name in d: d = d[name]
    try:
        if "created_at" in field: d = tweepy.utils.parse_datetime(d)
        if 'text' in field: d = d.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        return str(d)
    except:
        print("@@@Exception while extracting the field %s from the following object" % field)
        print(d)
        return "fail_to_convert_to_string"



if __name__ == '__main__':
    screen_name=get_profile_name()
    # Scrape the most recent N (up to 200) tweets authored by the given id
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    printList(tweets, tweet_cols, screen_name+'.tsv')
    print('Done!')

statuses = []
data = tweepy.Cursor(api.user_timeline, screen_name="rksriram91").items(max)
for status in data:
    statuses.append(status._json)
for status in tweepy.Cursor(api.user_timeline,screen_name="rksriram91").items():
    # process status here
    process_status(status)
	
