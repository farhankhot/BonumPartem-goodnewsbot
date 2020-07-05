import requests
import tweepy
import praw
import time
import json


# from bs4 import BeautifulSoup

twitter_consumer_key = ""
twitter_consumer_secret = ""
twitter_access_token = ""
twitter_access_token_secret = ""
reddit_client_id = ""
reddit_client_secret = ""

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

    def get_old_tweets(self):
        # get_previous_tweets = self.twitter_client.user_timeline(tweet_mode="extended")

        old_tweets_list=[]
        # Need to use tweepy.Cursor object otherwise run into pagination issues (it only gets first page tweets)
        for tweet in tweepy.Cursor(self.twitter_client.user_timeline, tweet_mode="extended").items():
            for x in tweet._json['entities']['urls']:
                expanded_url = x['expanded_url']
                indices = x['indices']
                # print(x)
                # Twitter gives status text in form 'title''t.co url''expanded url'
                # This removes it by getting the indices of when the url starts and ends and replacing it with ''
                for indice in indices:
                    first_indice = indices[0]
                    second_indice = indices[1]
                text_of_tweet = tweet._json['full_text']
                new_s = "".join( (text_of_tweet[:first_indice], "", text_of_tweet[second_indice:]) )
                old_post="{}{}".format(new_s, expanded_url)
                old_tweets_list.append(old_post)

                # print(old_post)
                # print("" + new_s)
        old_tweets_set = set(old_tweets_list)
        # Prints old tweets (list cause it gives it in order)
        # for _ in old_tweets_list:
        #     print("old shit: " + _)
        return old_tweets_set

    def get_reddit_posts(self):
        # Fetch new posts from reddit
        new_tweets_list=[]
        # How is limit divided for multiple subreddits ? Or is it random ? (Not a huge deal)
        for submission in self.reddit_client.subreddit("UpliftingNews+Positive_News").hot(limit=50):
            # 200 cause when its 280 twitter doesn't give the full text and gives a twitter status url
            # of the tweet which makes the set difference method think its new and therefore tries to post it which
            # gives a 'status duplicate error' (not sure about this anymore)
            if (len(submission.title) < 200 ):
                # Changing & to and cause twitter does some fucky shit
                processed_title = submission.title.replace("&", "and")

                post = "{} {}".format(processed_title, submission.url)
                new_tweets_list.append(post)
            # print(proxcessed_title)
        new_tweets_set = set(new_tweets_list)
        # Print fetched posts from reddit
        # for _ in new_tweets_set:
        #     print("fetched shit: " + _)
        return new_tweets_set

    def post_tweets(self):
        final_tweets = set()
        # final_tweets = new_tweets_set.difference(old_tweets_set)
        final_tweets = self.get_reddit_posts().difference(self.get_old_tweets())

        # Post and print unique (not already posted) tweets
        if len(final_tweets) > 0:
            print("how many new posts: %s " % (len(final_tweets) ))
            for tweet in final_tweets:
                # print("posting new tweet: " , tweet )
                # print (type(tweet))
                self.twitter_client.update_status(tweet)
        else:
            print("no new stuff: %s" % len(final_tweets)) # should be 0

        time.sleep(60)

if __name__ == '__main__':
    bot = GoodNewsBot()
    while True:
        bot.post_tweets()
