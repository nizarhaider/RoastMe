import pandas as pd

def clean(file):
    df = pd.read_csv(file, index_col=None)

    print((df))
    indexEmpty = df[df["comments"].isin(["[]"])].index
    df.drop(indexEmpty , inplace=True)
    print(df)
    print(len(df))
    df.to_csv('cleaned_output.csv')
    return 10

clean("output.csv")