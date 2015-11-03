#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: install.py
# Description : This program is used to fetch labeled tweets
# Twitter currently limits such requests to 180/window (15 minutes). To be on the
# safe side, we use 150/window.
#######################################################################

import csv, getpass, json, os, time, urllib
import requests
from requests_oauthlib import OAuth1
from os.path import exists
import os.path
import sys


#define the dir here
inputDir = './labelData.csv'
rawDir = './rawdata'

#changed your key here
CONSUMER_KEY = '6sdz4Asc6Kxszi4zB0AnMHGkC'
CONSUMER_SECRET = 'jiM3QdILuiCjnmteCm3UDVTTAiWDIJdBsk3ham1A8Lqe7Ex4CE'

OAUTH_TOKEN = '3163929288-PIHT99H2DGqxwamsGNQlL5NfjZkjBgH5wUmXUmW'
OAUTH_TOKEN_SECRET = 'tev5R42Kxrw2SsE6R4zMd0U2kdUTH5J11UcgtKqtcrqpE'

# function used to get the tweets id list
def get_list(in_filename):

    tweets_id = []
    with open(in_filename,'rb') as f:

        myreader = csv.reader(f,delimiter=',')

        #skip the header
        next(myreader, None)

        for tweetsid,value in myreader:
            tweets_id.append(tweetsid)
    
    return tweets_id


def get_time_left_str( cur_idx, fetch_list, download_pause ):

    tweets_left = len(fetch_list) - cur_idx
    total_seconds = tweets_left * download_pause

    str_hr = int( total_seconds / 3600 )
    str_min = int((total_seconds - str_hr*3600) / 60)
    str_sec = total_seconds - str_hr*3600 - str_min*60

    return '%dh %dm %ds' % (str_hr, str_min, str_sec)

# get oauth
def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

# used to download the tweets
def download_tweets( fetch_list, raw_dir ):

    # ensure raw data directory exists
    if not os.path.exists( raw_dir ):
        os.mkdir( raw_dir )

    # stay within rate limits
    max_tweets_per_hr  = 150*4
    download_pause_sec = 3600 / max_tweets_per_hr

    oauth = get_oauth()

    # download tweets
    for idx in range(0,len(fetch_list)):

        # current item
        item = fetch_list[idx]

        # print status
        trem = get_time_left_str( idx, fetch_list, download_pause_sec )
        print '--> downloading tweet #%s (%d of %d) (%s left)' % \
              (item, idx+1, len(fetch_list), trem)

        #data url
        myurl = 'https://api.twitter.com/1.1/statuses/show/' +item+'.json'

        # pull data
        data = requests.get(url=myurl, auth=oauth).json()

        with open(raw_dir+'/' + item + '.json', 'wb') as outfile:
          json.dump(data, outfile)
          
        # stay in Twitter API rate limits 
        print '    pausing %d sec to obey Twitter API rate limits' % \
              (download_pause_sec)
        time.sleep( download_pause_sec )

    return

#get the label of tweets
def get_label(in_file):

    label_tweets = {}

    with open(in_file,'rb') as f:

        myreader = csv.reader(f,delimiter=',')

        for tweetid,label in myreader:

            if label == '1':
                label_tweets[tweetid] = 1
            elif label == '-1':
                label_tweets[tweetid] = -1
            elif label == '0':
                label_tweets[tweetid] = 0

    return label_tweets

#get tweets from download file
def get_tweets(rawDir):

    file_name_list = []

    file_name_list = os.listdir(rawDir)

    tweets_list = {}

    for each_file in file_name_list:

        file_abdir = rawDir + '/'+each_file
        with open(file_abdir,'r') as f :
            tweets = json.loads(f.read())
            tweets_name = each_file.split('.')[0]
            if 'text' in tweets.keys():
                tweets_list[tweets_name] = tweets['text']

    return tweets_list

def combine(tweets_list,label_tweets):

    postiveTweets = 0
    negativeTweets = 0
    neutralTweets = 0

    for tweetid in tweets_list.keys():
        if tweetid in label_tweets.keys():
            storeData = [tweets_list[tweetid].encode('ascii', 'ignore'),label_tweets[tweetid]]
            writ_trainData(storeData)

            if storeData[1] == 0:
                neutralTweets +=1
            elif storeData[1] == 1:
                postiveTweets += 1
            else:
                negativeTweets += 1
    
    print "AllDone! - positive: %i - neutral: %i - negative:%i" %(postiveTweets,neutralTweets,negativeTweets)


#write into file 
def writ_trainData(doc):

    if not os.path.exists('trainDataSet.csv'):
        with open('trainDataSet.csv','w') as f:
            writehead = csv.writer(f,lineterminator='\n')
            writehead.writerow(['content','label'])
    
    with open('trainDataSet.csv','ab') as f:
        write = csv.writer(f,lineterminator='\n')
        write.writerow(doc) 

if __name__ == '__main__':

    #get tweets list
    tweetsList = get_list(inputDir)

    #start fetching data from twitter
    download_tweets(tweetsList, rawDir)

    # GET LABEL
    label = get_label(inputDir)

    # GET TWEETS
    tweets = get_tweets(rawDir)

    # out put the file
    combine(tweets,label)


