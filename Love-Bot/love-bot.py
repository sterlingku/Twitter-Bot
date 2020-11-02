# requirements:
# tweet back at user with a phrase from a dictionary such as 'i love you', 'don't hurt yourself'
# after x amount of tweets to LoveBot, ask if they need resources.  if yes, respond with resources for them to call
# randomly post about mental health facts daily
# keep track of who tweeted, when they tweeted, how many times, and what was tweeted to them
# cooldown tweeting to prevent spamming
# crawls tweets and looks for keywords like 'depression' or 'suicide'

import time
import tweepy
import random
import os
from dotenv import load_dotenv


# testing locally via .env file
load_dotenv()
API_CONSUMER_KEY = os.getenv('API_CONSUMER_KEY')
API_CONSUMER_SECRET = os.getenv('API_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
tweet_log = 'tweet_log.txt'
quotes_file = 'quotes.txt'


class Solution:

    # def __init__(self):
    #     self.id = None
    #     self.user.screen_name = None
    #     self.full_text = None

    # store metadata in a log, so bot knows what it has done so far
    def store_tweet_log(self, mention_id, screen_name, full_text, tweet_log):
        with open(tweet_log, 'r') as f:
            if str(mention_id).strip() in f.read():
                f.close()
                return False
            else:
                f_write = open(tweet_log, 'a')
                f_write.write('\n' + str(mention_id) + ' | ' + str(screen_name) + ' | ' + str(full_text))
                # f_write.write(' | ' + )
                f_write.close()
                return True

    # retrieve the latest mention.id, so bot knows where to continue
    def retrieve_last_replied(self):
        with open(tweet_log, 'r') as f:
            for line in f:
                since_id = line.split('|')[0]
        f.close()
        return since_id

    # retrieve a random quote from a file
    def retrieve_quote(self):
        f_read = open(quotes_file, 'r')
        lines = f_read.readlines()
        quote = random.choice(lines)
        return quote

    # reply to tweets
    def reply_to_tweets(self):
        print('Retrieving and replying to tweets...')
        since_id = self.retrieve_last_replied()
        print('Last replied to tweet was: ' + since_id)
        # all mentions since the latest since_id
        mentions = api.mentions_timeline(since_id, tweet_mode='extended')
        # displays all other metadata to expand upon
        print(mentions)
        # iterate through each mention in reverse to reply to older tweets first
        for mention in reversed(mentions):
            # reply to tweets that meet criteria below.  add regular expression if misspelling found instead
            if '#quote' in mention.full_text.lower():
                # pass all these parameters to the log if True
                if self.store_tweet_log(mention.id, mention.user.screen_name, mention.full_text, tweet_log):
                    print('Found #quote! Responding back and appending to log...')
                    print(str(mention.id) + ' | ' + mention.user.screen_name + ' | ' + mention.full_text)
                    quote = self.retrieve_quote()
                    api.update_status('@' + mention.user.screen_name + ' ' + quote, mention.id)
                else:
                    print('Already responded to this tweet!')
                # sleep for every 5 seconds
                time.sleep(5)

    # post tweets
    def post_tweets(self):
        print('Posting tweet of the day...')


tweet = Solution()
tweet.reply_to_tweets()
tweet.post_tweets()
