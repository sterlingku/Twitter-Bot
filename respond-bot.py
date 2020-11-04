import datetime
import time
import random
import tweepy
import os
from dotenv import load_dotenv

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

# files that need to exist
quotes = 'quotes.txt'
tweet_log = 'tweet_log.txt'


class Tweet:

    def reply_to_tweets(self):
        # while loop required to constantly run, otherwise script ends
        while True:
            print('Script is running. Now replying and liking tweets...')
            # retrieve the latest mention.id
            last_id = self.retrieve_seen_id()
            print('last_id is: ' + last_id)
            # all mentions since the latest mention.id
            mentions = api.mentions_timeline(last_id, tweet_mode='extended', count=5000)
            # iterate through each new mention in reverse to reply to older tweets first
            for mention in reversed(mentions):
                # print(mention)  # useful to find other metadata
                # print(tweepy.error.TweepError)  # prints error message and end the script, if any
                # reply to tweets that meet the criteria below
                if '#helloworld!' in mention.full_text.lower():
                    # pass all these parameters to the tweet_log
                    if self.store_tweet_log(mention.id, mention.user.screen_name, mention.full_text):
                        print('Found #helloworld! Responding back...')
                        print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text)
                        # respond with tweet
                        api.update_status('@' + mention.user.screen_name + ' HelloWorld back to you!', mention.id)
                        # favorite the tweet
                        api.create_favorite(mention.id)
                    else:
                        print('Already responded to this tweet! helloworld')
                    # sleep for 5 seconds before replying
                    time.sleep(5)
                if 'quote' in mention.full_text.lower() or 'quotes' in mention.full_text.lower():
                    if self.store_tweet_log(mention.id, mention.user.screen_name, mention.full_text):
                        print('Found quote! Responding back...')
                        print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text)
                        quote = self.retrieve_quote()
                        api.update_status('@' + mention.user.screen_name + ' ' + quote, mention.id)
                        api.create_favorite(mention.id)
                    else:
                        print('Already responded to this tweet! quote')
                    time.sleep(5)
                # if 'stats' in mention.full_text.lower():
                #     if self.store_tweet_log(mention.id, mention.user.screen_name, mention.full_text):
                #         print('Found stats! Responding back...')
                #         print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text)
                #         api.update_status('@' + mention.user.screen_name + stats)
                #     else:
                #         print('Already responded to this tweet! stats')
                #     time.sleep(5)
            # sleep for 12 seconds before re-running, due to rate limits
            time.sleep(15)

    # retrieve the last_seen_id, so bot knows where to continue
    def retrieve_seen_id(self):
        f_read = open(tweet_log, 'r')
        # tweet_log cannot start off blank or else it will error. Takes the last line as the value
        last_logged_tweet = f_read.readlines()[-1].split('|')
        last_seen_id = last_logged_tweet[0].strip()
        f_read.close()
        return last_seen_id

    # store metadata in a log, so bot knows what it has done so far
    def store_tweet_log(self, mention_id, screen_name, full_text):
        seen_ids = []
        with open(tweet_log) as f:
            # store mention_id in seen_ids
            for line in f:
                line_data = line.split('|')
                seen_ids.append(int(line_data[0].strip()))
            if mention_id not in seen_ids:
                f.close()
                f_write = open(tweet_log, 'a')
                f_write.write('\n' + str(mention_id) + ' | ' + str(datetime.datetime.now()) + ' | ' + str(screen_name) + ' | ' + str(full_text))
                f_write.close()
                return True
            else:
                f.close()
                return False

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
