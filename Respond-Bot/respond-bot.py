# must delete file_name log (except first line) and delete responses to tweets for this to work

import time
import tweepy


# testing locally via .env file
# import os
# from dotenv import load_dotenv
# load_dotenv()
# API_CONSUMER_KEY = os.getenv('API_CONSUMER_KEY')
# API_CONSUMER_SECRET = os.getenv('API_CONSUMER_SECRET')
# ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
# ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# stores the API keys in Heroku Config Vars
from os import environ
API_CONSUMER_KEY = environ['API_CONSUMER_KEY']
API_CONSUMER_SECRET = environ['API_CONSUMER_SECRET']
ACCESS_TOKEN_KEY = environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
file_name = 'last_seen.txt'


class Tweet:

    def reply_to_tweets(self):
        # while loop required to constantly run
        while True:
            print('Retrieving and replying to tweets...')
            last_id = self.retrieve_seen_id()
            # all mentions since the latest last_id
            mentions = api.mentions_timeline(last_id, tweet_mode='extended', count=5000)
            # iterate through each mention in reverse to reply to older tweets first
            for mention in reversed(mentions):
                print(mention)
                # reply to tweets that meet criteria below
                if '#helloworld!' in mention.full_text.lower():
                    self.store_seen_id(mention.id)
                    print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text)
                    print('Found #helloworld! Responding back...')
                    # prints an error, if any
                    print(tweepy.error.TweepError)
                    api.update_status('@' + mention.user.screen_name + ' HelloWorld back to you!', mention.id)
                    # sleep for 5 seconds before replying
                    time.sleep(5)
                else:
                    print('No new tweets.  Running again soon...')
            # sleep for 10 seconds before re-running
            time.sleep(10)

    # store the seen_id, so bot knows where to continue from next time
    def store_seen_id(self, seen_id):
        f_write = open(file_name, 'a')
        f_write.write('\n' + str(seen_id))
        f_write.close()
        return

    # retrieve the latest seen_id, so bot knows where to continue
    def retrieve_seen_id(self):
        f_read = open(file_name, 'r')
        # file_name needs value, or it will error.  Takes the last line as the value.  Don't leave empty lines
        last_seen_id = int(f_read.readlines()[-1].strip())
        # int(f_read[-1].read().strip())  # not needed
        f_read.close()
        return last_seen_id


# driver code needed for this to work
obj1 = Tweet()
obj1.reply_to_tweets()
