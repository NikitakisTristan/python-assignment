import os
import glob
import pandas as pd

# defining a local_folder path
local_folder = os.path.join(os.environ['USERPROFILE'], "Desktop\\FIRDS_Data\\")

# The glob module allows us to find all pathnames based on a matching pattern.
# In this case we are searching for all the files in our defined path that start with
# the string "FULNCR_20200808_D_" and are a .csv file. Then we call the glob method to
# return those paths.
selected_files = glob.glob(os.path.join(
    local_folder, "FULNCR_20200808_D_*.csv"))

# we setup a variable called all_dataframes as an empty list which we will append
# as we loop through each file
all_dataframes = []

# we loop through each file in our selected_files and call our panda module to
# read each .csv file and save it as a dataframe, df which we then append to our empty list
# object called all_dataframes. We are using dtype (data type) of "unicode" to reduce any errors
# that may come up as the pandas module reads through the values in our csv file.
for file in selected_files:
    df = pd.read_csv(file, sep=',', dtype="unicode")
    #df['file'] = file.split('/')[-1]
    all_dataframes.append(df)

# once we have looped through all the files and added each dataframe to our empty list
# we will then concatenate all the data frames together and export them as a new .csv file
# with a new name of "merged_FULNCR_20200808_D_data"
merged_dataframe = pd.concat(all_dataframes, ignore_index=True)
merged_dataframe.to_csv(r'' + local_folder +
                        'merged_FULNCR_20200808_D_data.csv')
