import os 
import glob as glob 
import pandas as pd


# Path to the folder containing the csv files
path = r"C:\Users\nizar\Documents\GitHub\RoastMe.ai\others\data_collection_and_preprocessing\combined"

# # print all csv files names in the folder using glob
# for files in glob.glob(os.path.join(path, "*.csv")):
#     print(files)

# function to combine all csv files in the list and remove duplicates
def combine_csv(list_of_csv):
    combined_csv = pd.concat([pd.read_csv(f) for f in list_of_csv ])
    combined_csv.drop_duplicates(subset ="image_url", keep = "first", inplace = True) 
    combined_csv.to_csv( "combined.csv", index=False, encoding='utf-8-sig')


list_of_csv = glob.glob(os.path.join(path, "*.csv")) # use glob to create the list of csv files

combine_csv(list_of_csv=list_of_csv)