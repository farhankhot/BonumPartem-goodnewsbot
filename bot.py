import requests
import tweepy
import praw
import time
import json


from bs4 import BeautifulSoup

twitter_consumer_key = "qXqWTRAOb1YnVk9gk7KBOBjSv"
twitter_consumer_secret = "YCMq1wbIXu12r1rX9LN5uTxlpCJ59QkrcioK0ktTpwrQmBojS7"
twitter_access_token = "1514550494-Al6a0LososSY2JASMwAgrJrPqINMylwoMbAe67A"
twitter_access_token_secret = "xkUBue8SDn4XCoqj2y76My6qA0iI4V9BHooSV2jubnU7x"
reddit_client_id = "lOk5XHqaCil21A"
reddit_client_secret = "dmZZPY47BPhV6mCzrmIA85oMEFg"

class GoodNewsBot:
    """docstring forGoodNews"""

    def __init__(self):
        self.twitter_client = self.auth_twitter_bot()
        self.reddit_client = self.init_reddit()

    def init_reddit(self):
        reddit = praw.Reddit(client_id = reddit_client_id,
        client_secret=reddit_client_secret,
        user_agent="Bonum Partem")
        return reddit

    # Set up twitter client
    def auth_twitter_bot(self):
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        #auth_url = auth.get_authorization_url()

        # Makes me verify each time, not needed when only posting to 1 account
        #verify_code = input("Authenticate at %s and then enter you verification code here: " % auth_url)
        #auth.get_access_token(verify_code)

        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        api = tweepy.API(auth)
        return api

    # ToDo: Refractor this function
    def get_titles(self):

        get_previous_tweets = self.twitter_client.user_timeline()

        old_tweets_dict={}
        old_tweets_list=[]
        for tweet in get_previous_tweets:
            for x in tweet._json['entities']['urls']:
                expanded_url = x['expanded_url']
                indices = x['indices']
                # Twitter gives status text in form 'title''t.co url''expanded url'
                # This removes it by getting the indices of when the url starts and ends and replacing it with ''
                for indice in indices:
                    first_indice = indices[0]
                    second_indice = indices[1]
                text_of_tweet = tweet._json['text']
                new_s = "".join( (text_of_tweet[:first_indice], "", text_of_tweet[second_indice: - 1]) )
                # Doesnt have form {}:{} like new_tweets_list because twitter for some reason adds the :
                # Automatically when there is text and a url in a tweet
                old_post="{}{}".format(new_s, expanded_url)
                old_tweets_list.append(old_post)

            # print(expanded_url)
            # print("new formatted string: " + new_s)

        old_tweets_set = set(old_tweets_list)
        # Prints old tweets
        # for _ in old_tweets_list:
        #     print("old shit: " + _)

        # Fetch new posts from reddit
        new_tweets_list=[]
        for submission in self.reddit_client.subreddit("UpliftingNews").hot(limit=10):
            # 116 cause when its 140 or even 120 twitter doesn't give the full text and gives a twitter status url
            # of the tweet which makes the set difference method think its new and therefore tries to post it which
            # gives a 'status duplicate error'
            if (len(submission.title) < 116 ):
                # Changing & to and cause twitter does some fucky shit
                processed_title = submission.title.replace("&", "and")
                post = "{}:{}".format(processed_title, submission.url)
                new_tweets_list.append(post)

        new_tweets_set = set(new_tweets_list)
        # Print fetched posts from reddit
        # for _ in new_tweets_list:
        #     print("fetched shit: " + _)

        final_tweets = set()
        final_tweets = new_tweets_set.difference(old_tweets_set)

        # Post and print unique (not already posted) tweets
        if len(final_tweets) > 0:
            print("how many new posts: %s " % (len(final_tweets) ))
            for tweet in final_tweets:
                print("new shit posting: " , tweet )
                # print (type(tweet))
                self.twitter_client.update_status(tweet)
        else:
            print("no new stuff: %s" % len(final_tweets)) # should be 0

        time.sleep(10)

if __name__ == '__main__':
    bot = GoodNewsBot()
    while True:
        bot.get_titles()
