"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Create index for access to public services

"""
import pandas as pd

### Data frames with location data ###
# Read in parks data and add acreage data to the geocoded parks data
parks = pd.read_csv("../data/geocoded/parks_geocoded.csv", dtype = str)
parks_acreage = pd.read_csv("../data/original/CPD_Parks.csv", 
                            dtype = {"PARK_NO": str, "ACRES": float},
                            usecols = ["PARK_NO", "ACRES"])
parks_acreage = parks_acreage.rename(columns = {"PARK_NO":"ID", "ACRES": "Park Acres"})

# Only keep rows with acreage data
parks = parks.join(parks_acreage.set_index("ID"), on = "ID", how = "inner")

# Read in other public services data
libraries = pd.read_csv("../data/geocoded/libraries_geocoded.csv", dtype = str,
                        usecols = ["Tract"])
bus_stops = pd.read_csv("../data/geocoded/bus_geocoded.csv", dtype = str,
                        usecols = ["Tract"])
L_stops = pd.read_csv("../data/geocoded/l_stops_geocoded.csv", dtype = str,
                      usecols = ["Tract"])
divvy = pd.read_csv("../data/geocoded/divvy_geocoded.csv", dtype = str,
                    usecols = ["Tract"])

# Read in census data for population information
census_data = pd.read_csv("../data/original/acs5_data_2022.csv",
                          dtype = {"Tract Code": str, "Total Pop (#)": int},
                          usecols = ["Tract Code", "Total Pop (#)"])
census_data = census_data.rename(columns = {"Tract Code": "Tract",
                                            "Total Pop (#)": "Total Pop"})

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
            df = df.groupby("Tract").sum("Park Acres").reset_index()
        else:
            count_col_name = key + " " + "Count"
            df = df.groupby("Tract").size().to_frame(count_col_name).reset_index()
        df = df.merge(pop_data, left_on = "Tract", right_on = "Tract")
        transformed_data[key] = df

    return transformed_data


def calculate_scores(df, df_name, service_col, n_bins, bin_labels):
    """
    Calculate score for each tract in a data set based on ratio of public services  
    to total population with thresholds based on distribution.  Scores are relative,
    calculated across all tracts.

    Inputs:
        df (pd): data to score
        df_name (str): name of dataframe
        service_col (str): column to base score on
        n_bins (int): number of bins to categorize rows (i.e. highest possible score)
        bin_labels (list of ints): labels for score options
    
    Returns:
        df_short (pd): dataframe with score column and tracts with 0 population dropped
    """
    # Divide count or acres by total population
    index_pop_0 = df[df["Total Pop"] == 0].index 
    df_short = df.drop(index_pop_0)
    df_short["proportion"] = df_short[service_col] / df_short["Total Pop"]

    # Find distribution of proportion and split into 5 groups for transit or 15
    # for parks and libraries
    thresholds = pd.cut(df_short["proportion"], bins = n_bins, labels = bin_labels)

    # Name the score column and convert scores to integer
    col_name = df_name + " " + ("Score")
    df_short[col_name] = thresholds.astype(int)
    df_short = df_short.drop(columns = ["proportion"])

    return df_short


def produce_indexed_data(services_data: dict, pop_data: pd):
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
            df_scored = calculate_scores(df, key, "Park Acres", 100, list(range(1,101)))
        elif key == "Libraries":
            df_scored = calculate_scores(df, key, "Libraries Count", 100, list(range(1,101)))
        else:
            count_col_name = key + " " + "Count"
            df_scored = calculate_scores(df, key, count_col_name, 100, list(range(1,101)))
        scored_data[key] = df_scored

    # Make one dataframe where each row is a census tract and the columns are 
    # public service statistics
    full_index_df =  pd.concat([scored_data["Parks"], scored_data["Libraries"], 
                                scored_data["Bus"], scored_data["L"],
                                scored_data["Divvy"]])
    
    # Give NaNs a score of 0
    full_index_df = full_index_df.fillna(0)

    # Group scores by census tract
    full_index_df = full_index_df.groupby("Tract").sum()

    # Create an overall transit score column
    full_index_df["Transit Count"] = (full_index_df["Bus Count"] + \
        full_index_df["L Count"] + full_index_df["Divvy Count"])
    full_index_df = calculate_scores(full_index_df, "Transit", "Transit Count", \
                                    100, list(range(1,101)))

    # Calculate index as weighted average
    full_index_df["APS Index"] = ((full_index_df["Parks Score"] / 100) * 0.3333) + \
                    ((full_index_df["Libraries Score"] / 100) * 0.3333) + \
                    ((full_index_df["Transit Score"] / 100) * 0.3333)

    full_index_df = full_index_df.reset_index()

    # Rejoin shortened data without 0 population rows with the data with 0
    # population
    pop_0_bus = linked_data["Bus"][linked_data["Bus"]["Total Pop"] == 0]
    pop_0_l = linked_data["L"][linked_data["L"]["Total Pop"] == 0]
    pop_0_df =  pd.concat([pop_0_bus, pop_0_l])
    pop_0_df = pop_0_df.fillna(0)
    pop_0_df = pop_0_df.groupby("Tract").sum().reset_index()
    pop_0_df = pop_0_df.drop(columns = ["Total Pop"])

    full_index_df = pd.concat([full_index_df, pop_0_df])
    full_index_df = full_index_df.loc[:,["Tract", "Total Pop", "Park Acres", 
                                         "Parks Score", "Libraries Count", 
                                         "Libraries Score", "Bus Count", 
                                         "Bus Score", "L Count", "L Score", 
                                         "Divvy Count", "Divvy Score",
                                         "Transit Score", "APS Index"]]
    full_index_df = full_index_df.rename({"Bus Count": "Bus Stop Count",
                                          "L Count": "L Stop Count",
                                          "Divvy Count": "Divvy Station Count"})
    
    return full_index_df

indexed_data = produce_indexed_data(dataframes, census_data)
indexed_data.to_csv("../data/index_data.csv", index = False)
