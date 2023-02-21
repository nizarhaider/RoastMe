import asyncio
import time
import praw
import asyncpraw
import pandas as pd
from tqdm import tqdm
import os
import time
import concurrent.futures
from tqdm import tqdm

reddit = praw.Reddit(
    client_id="m_zO2sVNL0uFZ-5U2grDVg",
    client_secret="O11TNu-7b-obob1c_i7q2-3WeBfZag",
    username="2broke2code",
    password="Fonseka12",
    user_agent="android:com.2broke2code.roastbot:v1.1.1 (by u/2broke2code)",
)

all_ids = []

# Path to the folder containing the JSON files
folder_path = "converted"

def extract_submission_objects(ids):
    submissions = []
    for submission_id in tqdm(ids, desc="Extracting submissions", total=len(ids)):

        try:
            submission = reddit.submission(id=submission_id)
            if submission.url and submission.comments:
                submissions.append(submission)
        
        except Exception as e:
            print(e)
            continue

    return submissions


# Define the function for extracting image URLs and comments from a submission object
def extract_submission_data(submission):
    image_url = submission.url
    comments = [f"[{comment.body}]" for comment in submission.comments[1:5]]
    return (image_url, comments)


# Loop through all files in the folder
for filename in os.listdir(folder_path):

    if filename.endswith(".json"):
        # Construct the full file path by joining the folder path and file name
        file_path = os.path.join(folder_path, filename)
        
        # Open the file and read the JSON data into a DataFrame
        with open(file_path) as f:
            data = pd.read_json(f, lines=True)
            
            # Extract the IDs from the DataFrame and add them to the list
            all_ids.extend(data["id"].tolist())

csv_file_path = 'output.csv'
submission_ids = all_ids

try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=['image_url', 'comments'])
    df.to_csv(csv_file_path, index=False)

# Batch the submission IDs into chunks of 100
# submission_id_batches = [submission_ids[i:i+100] for i in range(0, len(submission_ids), 100)]

submission_id_batches = [submission_ids[i:i+100] for i in range(0, len(submission_ids), 100)]

# Loop over the submission ID batches and extract data using multithreading
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for batch in tqdm(submission_id_batches, desc="Extracting data", total=len(submission_id_batches)):
        submissions = executor.submit(extract_submission_objects, batch).result()
        submission_data = [extract_submission_data(submission) for submission in submissions]
        df = pd.DataFrame(submission_data, columns=['image_url', 'comments'])
        df.to_csv(csv_file_path, index=False, mode='a', header=False)

print("Done!")