import pandas as pd
import random

def replace_deleted_comments(df, replacement_sentences):
    # Define a lambda function to replace [deleted] and [removed] with a random sentence
    # Also, drop rows containing the string "https://www.reddit.com/r/RoastMe/about/rules/"
    replace_func = lambda comment: comment.replace('[deleted]', random.choice(replacement_sentences)).replace('[removed]', random.choice(replacement_sentences)) if ('so that we may review it.' not in comment) and len(comment) >= 100 else ''
    
    # Apply the lambda function to the 'comments' column
    df['comments'] = df['comments'].apply(replace_func)
    
    # Drop rows with empty comments
    df = df[df['comments'] != '']
    
    return df


def clean(file):

    df = pd.read_csv(file, index_col=False)
    indexEmpty = df[df["comments"].isin(["[]", 
                "https://www.reddit.com/r/RoastMe/about/rules/"])].index
    df.drop(indexEmpty , inplace=True)


    replacement_sentences = ['If I throw a stick, will you leave me too?.', 'Sorry I can’t think of an insult dumb enough for you to understand.', 'You are like a software update. every time I see you, I immediately think “not now”.', 'I look at you and think what a waste of two billion years of the evolution.', 
                             'Everyone has purpose in this life, yours is to become an organ donor.', 'Hurting you is the least thing I want to do… but it’s still in the list.']

    # Replace all instances of [deleted] in the 'comments' column with a random sentence
    df = replace_deleted_comments(df, replacement_sentences)
    df.to_csv('cleaned_output.csv', index=False)
    print(f"After Conversion: {len(df)}")

    return 10



clean("output.csv")