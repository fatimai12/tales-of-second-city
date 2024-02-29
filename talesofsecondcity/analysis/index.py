"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Create index for access to public services

"""
import pandas as pd 

### Data frames with location data ###
# Read in parks data and add acreage data to the geocoded parks data
parks = pd.read_csv("../data/transformed/parks_final.csv", dtype = str)
parks_acreage = pd.read_csv("../data/original/CPD_Parks.csv", 
                            dtype = {"PARK_NO": str, "ACRES": float},
                            usecols = ["PARK_NO", "ACRES"])
parks_acreage = parks_acreage.rename(columns = {"PARK_NO":"ID", "ACRES": "Acres"})

# Only keep rows with acreage data
parks = parks.join(parks_acreage.set_index("ID"), on = "ID", how = "inner")

# Read in other public services data
libraries = pd.read_csv("../data/transformed/libraries_final.csv", dtype = str,
                        usecols = ["Tract"])
bus_stops = pd.read_csv("../data/test_data/bus_test_data.csv", dtype = str,
                        usecols = ["TRACT"])
bus_stops = bus_stops.rename(columns = {"TRACT": "Tract"})
L_stops = pd.read_csv("../data/test_data/L_test_data.csv", dtype = str,
                      usecols = ["TRACT"])
L_stops = L_stops.rename(columns = {"TRACT": "Tract"})
divvy = pd.read_csv("../data/test_data/divvy_test_data.csv", dtype = str,
                    usecols = ["Tract Code"])
divvy = divvy.rename(columns = {"Tract Code": "Tract"})

# Read in census data for population information
census_data = pd.read_csv("../data/test_data/census22_test_data.csv",
                          dtype = {"Tract Code": str, "Total Pop": int},
                          usecols = ["Tract Code", "Total Pop"])
census_data = census_data.rename(columns = {"Tract Code": "Tract"})

# Put all data frames in a dictionary
dataframes = {"Parks": parks, "Libraries": libraries, "Bus": bus_stops,
              "L": L_stops, "Divvy": divvy}

### Functions to compute index ###
def link_data(services_data, pop_data):
    """
    Transforms public services data into census tract groups and links to 
    census data that includes total population

    Inputs:
        services_data (dict of pds): dictionary of public service dataframes
        pop_data (pd): census data with total population per census tract

    Returns:
        transformed_data (dict of pds): dictionary of transformed data
    """
    # For each category group by census and get total acreage (for parks) or
    # count (for libraries and transit stops)
    transformed_data = {}
    for key, df in services_data.items():
        if key == "Parks":
            df = df.groupby("Tract").sum("Acres").reset_index()
        else:
            df = df.groupby("Tract").size().to_frame("Count").reset_index()
        df = df.merge(pop_data, left_on = "Tract", right_on = "Tract")
        transformed_data[key] = df

    return transformed_data


def calculate_scores(df, df_name, service_col, n_bins, bin_labels):
    """
    Calculate score for each tract in a data set based on ratio of public services  
    to total population with thresholds based on distribution.  Scores are relative.

    Inputs:
        df (pd): data to score
        df_name (str): name of dataframe
        service_col (str): column to base score on
        n_bins (int): number of bins to categorize rows (i.e. highest possible score)
        bin_labels (list of ints): labels for score options
    
    Returns:
        None.  Adds score as a column to df.
    """
    # Divide count or acres by total population
    df["proportion"] = df[service_col] / df["Total Pop"]

    # Find distribution of proportion and split into 5 groups for transit or 15
    # for parks and libraries
    thresholds = pd.cut(df["proportion"], bins = n_bins, labels = bin_labels)

    # Name the score column and convert scores to integer
    col_name = df_name + " " + ("Score")
    df[col_name] = thresholds.astype(int)
    df = df.drop(columns = ["proportion", "Total Pop", service_col])

    return df


def calculate_index(services_data: dict, pop_data: pd):
    """
    Calculates access to public services index based on previously calculated
    individual public service scores.
    
    Inputs:
        services_data (dict of pds): dictionary of public service dataframes
        pop_data (pd): census data with total population per census tract
 
    Returns:
        full_index_df (pd): df with columns "Tract", "Parks Score", 
        "Library Score", "Transit Score", and "APS Index".
    """
    linked_data = link_data(services_data, pop_data)
    scored_data = {}
    # Calculate scores for each public services data frame
    for key, df in linked_data.items():
        if key == "Parks":
            df = calculate_scores(df, key, "Acres", 15, list(range(1,16)))
        elif key == "Libraries":
            df = calculate_scores(df, key, "Count", 15, list(range(1,16)))
        else:
            df = calculate_scores(df, key, "Count", 5, list(range(1,6)))
        scored_data[key] = df

    # Make one dataframe where each row is a census tract and the columns are the 
    # access to public service scores
    full_index_df =  pd.concat([scored_data["Parks"], scored_data["Libraries"], 
                                scored_data["Bus"], scored_data["L"],
                                scored_data["Divvy"]])
    
    # Give NaNs a score of 0
    full_index_df = full_index_df.fillna(0)

    # Group scores by census tract
    full_index_df = full_index_df.groupby("Tract").sum()

    # Create an overall transit score column
    full_index_df["Transit Score"] = full_index_df["Bus Score"] + \
        full_index_df["L Score"] + full_index_df["Divvy Score"]
    full_index_df = full_index_df.drop(columns = ["Bus Score", "L Score", "Divvy Score"])

    # Create an overall access to public service score
    full_index_df["Total Score"] = full_index_df["Parks Score"] + \
        full_index_df["Libraries Score"] + full_index_df["Transit Score"]

    # Normalize score as index from 0 to 1 and save file as csv
    full_index_df["APS Index"] = full_index_df["Total Score"] / 45
    full_index_df = full_index_df.reset_index()

    return full_index_df

indexed_data = calculate_index(dataframes, census_data)
indexed_data.to_csv("../data/indexed_data.csv", index = False)
