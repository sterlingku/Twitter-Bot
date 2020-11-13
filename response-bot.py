import os
import datetime
import time
import random
import pymongo
# import dnspython
from dotenv import load_dotenv
from pymongo import MongoClient
import tweepy


# required for loading from .env or Heroku Config Vars
load_dotenv()
API_CONSUMER_KEY = os.getenv('API_CONSUMER_KEY')
API_CONSUMER_SECRET = os.getenv('API_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# setting up API connection
auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URL'))
# access created MongoDB database via variable 'db'
db = client.tweet_log

# database connection message
try:
    conn = MongoClient()
    print('Successfully connected to MongoDB')
except:
    print('Failed to connect to MongoDB.')


# files that need to exist
quotes = 'quotes.txt'


class Tweet:

    def reply_to_tweets(self):
        # while loop required to constantly run, otherwise script ends
        while True:
            print('Script is running. Now replying and liking tweets...')
            # retrieve the latest mention.id
            last_mention_id = self.retrieve_last_created_at()
            print('last mention_id: ' + last_mention_id)
            # all mentions since the latest mention.id
            mentions = api.mentions_timeline(last_mention_id, tweet_mode='extended', count=5000)
            # iterate through each new mention in reverse to reply to older tweets first
            for mention in reversed(mentions):
                # print(mention)  # useful to find other metadata
                # print(tweepy.error.TweepError)  # prints error message and end the script, if any
                # pass all these parameters to the tweet_log if not already in DB
                if self.store_tweet_log(mention.id, mention.user.screen_name, mention.full_text, mention.created_at):
                    # reply to tweets that meet the criteria below
                    if '#helloworld!' in mention.full_text.lower() or '#helloworld' in mention.full_text.lower():
                        print('Found #helloworld! Responding back...')
                        print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text + ' - ' + str(mention.created_at))
                        # respond with tweet
                        api.update_status('@' + mention.user.screen_name + ' HelloWorld back to you!', mention.id)
                        # favorite the tweet
                        api.create_favorite(mention.id)
                    if 'quote' in mention.full_text.lower() or 'quotes' in mention.full_text.lower():
                        print('Found quote! Responding back...')
                        print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text + ' - ' + str(mention.created_at))
                        quote = self.retrieve_quote()
                        api.update_status('@' + mention.user.screen_name + ' ' + quote, mention.id)
                        api.create_favorite(mention.id)
                    # if 'stats' in mention.full_text.lower():
                        # print('Found stats! Responding back...')
                        # print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text + ' - ' + str(mention.created_at))
                        # api.update_status('@' + mention.user.screen_name + stats)
                        # api.create_favorite(mention.id)
                # sleep for 5 seconds before replying, to be respectful of server
                time.sleep(5)
            # sleep for 12 seconds before re-running, due to rate limits
            time.sleep(15)

    # retrieve the latest mention_id, so bot knows where to continue
    def retrieve_last_created_at(self):
        # count to find if there is any data in tweets collection
        tweet_count = db.tweets.count()
        if tweet_count == 0:
            db.tweets.insert({'mention_id': 1234567890,
                              'screen_name': 'dummy_insert',
                              'full_text': 'dummy text',
                              'created_at': '2000-01-01T00:00:00',
                              'responded_at': datetime.datetime.now()
                              })
        # required to access elements in the dict
        tweet_data = db.tweets.find().limit(1).sort([('mention_id', -1)])
        # returns the latest created_at date
        for mention_id in tweet_data:
            return str(mention_id.get('mention_id'))

    # store metadata in the db, so bot knows what it has done so far
    def store_tweet_log(self, mention_id, screen_name, full_text, created_at):
        # don't need this in theory if last_created_at date works, but a good preventative measure for duplicates
        exist = db.tweets.find({'mention_id': mention_id}).count()
        if exist >= 1:
            print(str(mention_id) + ' already exists in MongoDB')
            return False
        else:
            # insert values into db
            db.tweets.insert({'mention_id': mention_id,
                              'screen_name': screen_name,
                              'full_text': full_text,
                              'created_at': created_at,
                              'responded_at': datetime.datetime.now()
                              })
            return True

    # retrieve a random quote from quotes file
    def retrieve_quote(self):
        # encoding='cp1252' required for Heroku because txt file is in utf-8
        f_read = open(quotes, 'r', encoding='cp1252')
        lines = f_read.readlines()
        quote = random.choice(lines)
        return quote


# driver code needed for this to work
tweet = Tweet()
tweet.reply_to_tweets()
