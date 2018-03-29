#! /usr/bin/env python3

import os
import praw

if __name__ == "__main__":
    praw_client_id = os.environ['PRAW_CLIENT_ID']
    praw_secret = os.environ['PRAW_SECRET']
    praw_user_id = os.environ['PRAW_USER_ID']
    praw_password = os.environ['PRAW_PASSWORD']

    print("Client ID {}".format(praw_client_id))
    print("Secret {}".format(praw_secret))
    print("User ID {}".format(praw_user_id))
    print("Password {}".format(praw_password))
                
    reddit = praw.Reddit(client_id=praw_client_id,
                         client_secret=praw_secret,
                         password=praw_password,
                         user_agent='personal_use',
                         username=praw_user_id)
    
    print(reddit.user.me())
    submission = reddit.submission(url="https://www.reddit.com/r/AskEngineers/comments/87vtyy/electrical_engineering_has_a_0_job_growth_rate/")
    for top_level_comment in submission.comments:
        print(top_level_comment.body)
