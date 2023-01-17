import praw
import pandas as pd
from tqdm import tqdm

reddit = praw.Reddit(
    client_id="m_zO2sVNL0uFZ-5U2grDVg",
    client_secret="O11TNu-7b-obob1c_i7q2-3WeBfZag",
    user_agent="android:com.2broke2code.roastbot:v1.1.1 (by u/2broke2code)",
)

subreddit = reddit.subreddit("RoastMe")
hot_posts = subreddit.hot(limit=1000)

# Create an empty list to store the data
data = []

# Iterate through the hot posts in the subreddit
for submission in tqdm(hot_posts,total=1000,desc='Scraping Posts'):

    post_data = {"image_url":submission.url}
    comments = submission.comments[1:10]
    comment_bodies = []
    for comment in comments:
        comment_bodies.append(f"[{comment.body}]")

    post_data["comments"] = comment_bodies
    data.append(post_data)

# Create a dataframe from the list
df = pd.DataFrame(data)

# print the dataframe
print(df)

df.to_csv('data_2000.csv', index=False)


