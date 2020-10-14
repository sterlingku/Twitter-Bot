# must delete file_name log (except first line) and delete responses to tweets for this to work

import time
import tweepy

# Bearer token = 'AAAAAAAAAAAAAAAAAAAAAB%2BqIAEAAAAAmBwuUMjqBPKSQKIe5qF62KMClJM%3DodxsB1NgXdkNj3k9BHc7rL9He5xkoqd3Q66MxUykxlVxPecwHA'
API_CONSUMER_KEY = 'IV3rcg6kUyU5bZqWCmJH2RPOb'
API_CONSUMER_SECRET = 'yP9VNahI9jSlSNvjvKDra1882ryIpbZwWk25LqQVDS6T18zC4r'
ACCESS_TOKEN_KEY = '1310750946025115648-GHlX2WHvozVdUFnrOkf7rmh6IMnVTX'
ACCESS_TOKEN_SECRET = 'XhwsHMES7tFPHIDpL9ncT954H14lBxUg6bzwyBQe72TH3'

auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
file_name = 'last_seen.txt'


class Solution:

    # store the seen_id, so bot knows where to continue from next time
    def store_seen_id(self, seen_id, file_name):
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

    def reply_to_tweets(self):
        print('Retrieving and replying to tweets...')
        last_id = self.retrieve_seen_id()
        # all mentions since the latest last_id
        mentions = api.mentions_timeline(last_id, tweet_mode='extended', count=5000)
        # iterate through each mention in reverse to reply to older tweets first
        for mention in reversed(mentions):
            print(mention)
            # reply to tweets that meet criteria below
            if '#helloworld!' in mention.full_text.lower():
                self.store_seen_id(mention.id, file_name)
                print(str(mention.id) + ' - ' + mention.user.screen_name + ' - ' + mention.full_text)
                print('Found #helloworld! Responding back...')
                # prints an error, if any
                print(tweepy.error.TweepError)
                api.update_status('@' + mention.user.screen_name + ' HelloWorld back to you!', mention.id)
                # sleep for every 5 seconds
                time.sleep(5)


obj1 = Solution()
obj1.reply_to_tweets()