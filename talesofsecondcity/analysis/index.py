"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Create index for access to public services

"""
import pandas as pd 

# Data frames with location data
parks = pd.read_csv("../data/transformed/parks_geocoded.csv", dtype = str, usecols = ["id", "tract"])
parks = parks.set_index("PARK_NO")
parks_acreage = pd.read_csv("../data/original/CPD_Parks.csv",
                            usecols = ["PARK_NO", "ACRES"])
parks_acreage = parks_acreage.set_index("PARK_NO")
parks = parks.join(parks_acreage)

libraries = pd.read_csv("../data/transformed/libraries_geocoded.csv", dtype = str,
                        usecols = ["Tract"])
bus_stops = pd.read_csv("../data/test_data/bus_test_data.csv", dtype = str,
                        usecols = ["Tract"])
L_stops = pd.read_csv("../data/test_data/L_test_data.csv", dtype = str,
                      usecols = ["Tract"])
divvy = pd.read_csv("../data/test_data/divvy_test_data.csv", usecols = ["Tract"])

census_data = pd.read_csv("../data/test_data/census22_test_data.csv",
                          usecols = ["Tract Code", "Total Pop"]) 

dataframes = {"Parks": parks, "Libraries": libraries, "Bus": bus_stops,
              "L": L_stops, "Divvy": divvy}


def link_data(services_data, pop_data):
    """
    Transforms public services data and links to census data

    Returns dictionary of transformed data
    """
    # For each category group by census and get total acreage (for parks) or
    # count (for libraries and transit stops)
    transformed_data = {}
    for key, df in services_data.items():
        if key == "Parks":
            df = df.groupby("Tract").sum().reset_index(name = "Total Acreage")
        else:
            df = df.groupby("Tract").count().reset_index(name = "Count")
        df = df.merge(pop_data, left_on = "Tract", right_on = "Tract Code")
        transformed_data[key] = df

    return transformed_data


def calculate_scores(df, df_name, service_col):
    """
    Calculate score for each tract in a data set based on proportion of services  
    to total population, and define thresholds

    Add score as a column for corresponding row with "Score"
    """
    # divide count by total population
    df["proportion"] = df[service_col] / df["Total Pop"]

    # find distribution of proportion and split into 5 groups 
    thresholds = pd.cut(df["proportion"], 5)
    level_1 = thresholds[0]
    level_2 = thresholds[1]
    level_3 = thresholds[2]
    level_4 = thresholds[3]
    level_5 = thresholds[4]

    col_name = df_name + "Score"
    df[col_name] = 0
    
    for index, row in df.iterrows():
        if row.proportion in level_1:
            df.at[index, col_name] = 1
        elif row.proportion in level_2:
            df.at[index, col_name] = 2
        elif row.proportion in level_3:
            df.at[index, col_name] = 3
        elif row.proportion in level_4:
            df.at[index, col_name] = 4
        elif row.proportion in level_5:
            df.at[index, col_name] = 5

    df = df.drop(columns = ["proportion", "Total Pop", service_col])

    return df


def calculate_index(services_data: dict, census_data: pd):
    """
    Calculates access to public services index
    
    Returns df with columns "Tract", "Parks Score", "Library Score", "Transit Score",
    and "APS Index"
    
    """
    linked_data = link_data(data, census_data)

    scored_data = {}
    # Calculate scores for each public services data frame
    for key, df in linked_data.items():
        if key == "Parks":
            df = calculate_scores(df, key, "Total Acreage")
            df = df.reset_index()
        else:
            df = calculate_scores(df, key, "Count")
        scored_data[key] = df

    # Make one dataframe where each row is a census tract and the columns are the 
    # service scores
    full_index_df =  pd.concat([scored_data["Parks"], scored_data["Libraries"], 
                                scored_data["Bus"], scored_data["L"],
                                scored_data["Divvy"]])
    full_index_df = full_index_df.groupby("Tract")


    full_index_df["Transit Score"] = full_index_df["Bus Score"] + \
        full_index_df["L Score"] + full_index_df["Divvy Score"]
    full_index_df = full_index_df.drop(columns = ["Bus Score", "L Score", "Divvy Score"])

    full_index_df["Total Score"] = full_index_df["Parks Score"] + \
        full_index_df["Libraries Score"] + full_index_df["Transit Score"]

    # normalize 0-1
    full_index_df["APS Index"] = full_index_df["Total Score"] / 45
