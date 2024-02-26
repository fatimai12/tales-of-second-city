"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Create index for access to public services

"""
import pandas as pd 

# Data frames with location data
parks = pd.read_csv("")
parks = parks.set_index("PARK_NO")
parks_acreage = pd.read_csv("", usecols = ["PARK_NO", "ACRES"])
parks_acreage = parks_acreage.set_index("PARK_NO")
parks = parks.join(parks_acreage)


libraries = pd.read_csv("")
bus_stops = pd.read_csv("")
L_stops = pd.read_csv("")
divvy = pd.read_csv("")

census_data = pd.read_csv("", usecols = ["TRACT", "TOTAL POP"]) 

dataframes = {"Parks": parks, "Libraries": libraries, "Bus": bus_stops,
              "L": L_stops, "Divvy": divvy}

THRESHOLDS = {"Parks": "low = , medium = , high =",
              "Libraries": "??",
              "Bus": "??",
              "L": "??",
              "Divvy": "??"}

def link_data(services_data, pop_data):
    """
    Transforms public services data and links to census data
    """
    # For each category group by census and get total acreage (for parks) or
    # count (for libraries and transit stops)
    for key, df in services_data.items():
        if key == "Parks":
            df = df.groupby("Tract").sum().reset_index(name = "Total Acreage")
        else:
            df = df.groupby("Tract").count().reset_index(name = "Count")
        df = df.merge(pop_data, left_on = "Tract", right_on = "Tract")

def calculate_scores(df, service_col):
    """
    Calculate score for each tract in a data set based on proportion of services  
    to total population, and define thresholds

    Add score as a column for corresponding row with "Score"
    """
    # divide count by total population
    df["proportion"] = df[service_col] / df["TOTAL POP"]
    # define thresholds for each category (look this up)
    # for index, row in df.iterrows():
    #    if row.proportion <
    # score census tract by thresholds


def calculate_index(data: dict):
    """
    Calculates access to public services index
    
    Returns df with columns "Tract", "Parks Score", "Library Score", "Transit Score",
    and "APS Index"
    
    """
    # Calculate scores for each public services data frame
    for key, df in data.items():
        if key == "Parks":
            calculate_scores(df, "Total Acreage")
            df = df.reset_index()
        else:
            calculate_scores(df, "Count")
        df = df.set_index("Tract")
        df = df[["Tract", "Score"]]

    # Make one dataframe where each row is a census tract and the columns are the 
    # service scores
    full_index_df =  pd.concat([data["Parks"], data["Libraries"], data["Bus"],
                                data["L"], data["Divvy"]])
    full_index_df.columns = ["Tract", "Parks Score"]

    full_index_df["Transit Score"] = full_index_df["Bus Score"] + \
        full_index_df["L Score"] + full_index_df["Divvy Score"]
    full_index_df = full_index_df.drop(columns = ["Bus Score", "L Score", "Divvy Score"])

    full_index_df["Total Score"] = full_index_df["Parks Score"] + \
        full_index_df["Libraries Score"] + full_index_df["Transit Score"]

    # normalize 0-1
    full_index_df["APS Index"] = full_index_df["Total Score"] / 45

    

