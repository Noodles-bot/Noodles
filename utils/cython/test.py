import pyximport

pyximport.install()
from utils.secret import *
import praw
import func


def main():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)
    print(type(reddit.subreddit('specialsnowflake').mod.log(limit=200000000, mod='Warrant3112')))
    print(len(func.actions(reddit.subreddit('specialsnowflake').mod.log(limit=200000000, mod='Warrant3112'))))


if __name__ == '__main__':
    main()
