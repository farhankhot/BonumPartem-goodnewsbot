import requests
import tweepy
import praw

from bs4 import BeautifulSoup
# from client import FeedlyClient

# URL = "https://worldsbestnews.tumblr.com/"
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
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        api = tweepy.API(auth)
        return api

    def get_titles(self):
        submissions={}
        # Will add more subs in the future
        for submission in self.reddit_client.subreddit("UpliftingNews").hot(limit=10):
            if (len(submission.title) > 140):
                continue
            else:
                submissions[submission.title] = submission.url
                
        # Post and Print each key value pair
        for key in submissions:
            tweet = "{}:{}".format(key, submissions[key])
            self.twitter_client.update_status(tweet)
            print(key, submissions[key])


    # Get the news
    #def get_posts(self):
        # page =requests.get("https://www.reddit.com/r/reddevils/")
        # soup = BeautifulSoup(page.content, 'html.parser')
        # pretty_soup = soup.prettify()
        # print(pretty_soup)

if __name__ == '__main__':
    bot = GoodNewsBot()
    bot.get_titles()
