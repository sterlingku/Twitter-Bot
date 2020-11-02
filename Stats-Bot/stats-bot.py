# requirements:
# tweet at the bot to see a list of stats for your account:
# who liked your tweets the most, most used hashtags, most @ user, day you tweet the most,


import tweepy
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
file_name = ''


class Words:

    def reply_to_tweets(self):
        # all mentions
        mentions = api.mentions_timeline(tweet_mode='extended')
        # displays all other mentions metadata to expand upon (useful: full_text, )
        for mention in reversed(mentions):
            print(mention)

    # general info about user
    def general_info(self, screen_name):
        info = api.get_user(screen_name)
        print(info)
        for api.key, api.value in info():
            print(api.key, ': ', api.value)

    # all accounts you are following
    def your_friends(self):
        count = 0
        friends = api.friends()
        for friend in friends:
            print(friend.screen_name)
            count += 1
        return count

    def your_followers(self):
        # all accounts following you
        count = 0



obj1 = Words()
#print(obj1.reply_to_tweets())
print(obj1.general_info('sterlingku'))
print(obj1.your_friends())
print(obj1.your_followers())
