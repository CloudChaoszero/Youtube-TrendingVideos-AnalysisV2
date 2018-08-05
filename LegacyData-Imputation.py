import os
import pandas as pd 
for files in os.listdir("Data/"):
    file_parts = files.split("-")
    date = file_parts[2].split(".")[0]
    day = date[-len(date)+1:-len(date)+2]
    year = date[-4:]
    month = date[-len(date):-len(date)+1]
    print(month, day, year)
    df = pd.read_csv(f"Data/{files}")

    if "RegionCode" not in list(df.columns):
        df["RegionCode"]=[file_parts[1] for i in range(df.shape[0])]

    if "Date" not in list(df.columns):

        df["Date"] = [f"{month}/{day}/{year}" for i in range(df.shape[0])]

    
    df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
    df.to_csv(f"Data/{files}")

if __name__=="__main__":
    print("Application Complete")