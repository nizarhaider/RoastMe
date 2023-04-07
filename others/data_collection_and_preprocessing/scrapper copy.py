import praw
import pandas as pd
from tqdm import tqdm
import os
import concurrent.futures


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
    user_agent=USER_AGENT,
)

all_ids = []

# Path to the folder containing the JSON files
folder_path = "converted"

# Loop through all json files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        # Construct the full file path by joining the folder path and file name
        file_path = os.path.join(folder_path, filename)
        
        # Open the file and read the JSON data into a DataFrame
        with open(file_path) as f:
            data = pd.read_json(f, lines=True)
            
            # Extract the IDs from the DataFrame and add them to the list
            all_ids.extend(data["id"].tolist())

def process_submission(submission_id):
    try:
        submission = reddit.submission(id=submission_id)
        if submission.url and submission.comments:
            comments = submission.comments[1:10]
            comment_bodies = []
            for comment in comments:
                comment_bodies.append(f"[{comment.body}]")

            return {"image_url": submission.url, "comments": comment_bodies}
    except Exception as e:
        print(f"Error retrieving submission with ID {submission_id}: {e}")
        return None     
    
            
# Create a DataFrame with the combined IDs
df = pd.DataFrame({"id": all_ids})


# Loop through the IDs and extract the desired information
output = []



with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(process_submission, submission_id) for submission_id in df["id"]]
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        result = future.result()
        if result is not None:
            output.append(result)


# Create a DataFrame with the output
output_df = pd.DataFrame(output)

# Write the results to a CSV file
output_df.to_csv("output.csv", index=False)
