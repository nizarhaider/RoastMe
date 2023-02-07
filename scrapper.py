import praw
import pandas as pd
from tqdm import tqdm
from pmaw import PushshiftAPI
import datetime as dt
import os

# to use PSAW

reddit = praw.Reddit(
    client_id="m_zO2sVNL0uFZ-5U2grDVg",
    client_secret="O11TNu-7b-obob1c_i7q2-3WeBfZag",
    user_agent="android:com.2broke2code.roastbot:v1.1.1 (by u/2broke2code)",
)
print("PRAW GOOD")

api_praw = PushshiftAPI(praw=reddit)

posts = api_praw.search_submissions(subreddit="science", limit=10)
post_list = [post for post in posts.id]
print(post_list)

# print("PUSHSHIFT GOOD")

# if os.path.exists("data_test.csv"):
#     # If the file exists, read the last timestamp from the file
#     df = pd.read_csv("data_test.csv")
#     ts_before = df['timestamp'].iloc[-1]
# else:
#     # If the file doesn't exist, use the current datetime
#     ts_before = dt.datetime.now().timestamp()
#     print(ts_before)
# print("Got date")
# # subreddit = reddit.subreddit("RoastMe")
# # hot_posts = subreddit.hot(limit=1000)

# # use PSAW only to get id of submissions in time interval
# gen = api.search_submissions(
#     until = ts_before, #October 1st
#     since = 1514764800,  #January 1st 
    
#     subreddit=['RoastMe'],
#     limit=100
# )
# print("Searched")


# # Create an empty list to store the data
# data = []

# # Iterate through the hot posts in the subreddit
# for submission_psaw in tqdm(gen, total=10,desc='Scraping Shit'):

# # for submission in tqdm(hot_posts,total=1000,desc='Scraping Posts'):
#     submission_id = submission_psaw.d_['id']
#     submission = reddit.submission(id=submission_id)

#     post_data = {"image_url": submission.url, "timestamp": submission.created_utc}
#     comments = submission.comments[1:10]
#     comment_bodies = []
#     for comment in comments:
#         comment_bodies.append(f"[{comment.body}]")

#     post_data["comments"] = comment_bodies
#     data.append(post_data)

# # Create a dataframe from the list
# df = pd.DataFrame(data)

# # print the dataframe
# print(df)

# # df.to_csv('data_test.csv', index=False)


