"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck and Fatima Irfan

Clean data that's been geocoded to use in index

"""
import pandas as pd
import re

def clean_parks(df):
    """
    Clean parks data.

    Inputs:
        df (pd): data frame of geocoded park data
    Returns:
        df (pd): cleaned geocoded parks data
    """
    # Keep only the ID and tract columns
    df = df[["ID", "Tract", "latitude", "longitude"]]

    # Remove the ".0" from the end of the tract column
    df = df.replace(to_replace = r'\.0$', value = "", regex = True)

    df["Tract"] = df["Tract"].astype(str)

    # Put leading zeros back in
    df["Tract"] = df["Tract"].str.zfill(6)

    df = df[["ID", "Tract", "latitude", "longitude"]]

    # Drop parks that could not be geocoded (n = 2)
    df = df.drop(df[df["Tract"].isnull()].index)
    df.to_csv("../data/geocoded/parks_geocoded.csv", index = False)

    return df

def clean_libraries():
    """
    Clean libraries data.

    Returns:
        libraries (pd): cleaned geocoded libraries data
    """
    # Read in geocoded libraries data
    libraries = pd.read_csv("../data/geocoded/libraries_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    libraries = libraries[["id", "tract", "latitude", "longitude"]]

    libraries["tract"] = libraries["tract"].astype(str)

    # Put leading zeros back in
    libraries["tract"] = libraries["tract"].str.zfill(6)

    # Rename columns to be consistent across all data
    libraries = libraries.rename(columns = {"id": "Name", "tract": "Tract"})
    libraries.to_csv("../data/geocoded/libraries_geocoded.csv", index = False)

    return libraries


def clean_l_stops(df):
    """
    Clean L stops data

    Inputs:
        df (pd): data frame of geocoded L stop data
    Returns:
        df (pd): cleaned geocoded L stop data
    """
    df[['latitude','longitude']] = df['Location'].str.strip("()").str.split(",", expand=True)

    #Keep only the ID and tract columns
    df = df[["STOP_NAME", "tract", "latitude", "longitude"]]

    # Rename columns to be consistent across all data
    df = df.rename(columns = {"STOP_NAME": "Name", "tract": "Tract"})

    df.to_csv("../data/geocoded/l_stops_geocoded.csv", index = False)

    return df

def clean_divvy(df):
    """
    Clean Divvy data

    Inputs:
        df (pd): data frame of geocoded Divvy station data
    Returns:
        df (pd): cleaned geocoded Divvy station data
    """    
    df["Tract"] = df["Tract"].astype(str)

    # Remove the ".0" from the end of the tract column
    df = df.replace(to_replace = r'\.0$', value = "", regex = True)

    # Put leading zeros back in
    df["Tract"] = df["Tract"].str.zfill(6)

    # Rename columns to be consistent across all data
    df = df.rename(columns = {"station_name": "Name"})

    df.to_csv("../data/geocoded/divvy_geocoded.csv", index = False)

    return df

def clean_bus(df):
    """
    Clean bus data

    Inputs:
        df (pd): data frame of geocoded bus stop data
    Returns:
        df (pd): cleaned geocoded bus stop data
    """

    df["Tract"] = df["Tract"].astype(str)
    
    # Remove the ".0" from the end of the tract column
    df = df.replace(to_replace = r'\.0$', value = "", regex = True)

    # Put leading zeros back in
    df["Tract"] = df["Tract"].str.zfill(6)

    #Keep only the ID and tract columns
    df = df[["public_nam", "Tract", "latitude", "longitude"]]

    # Rename columns to be consistent across all data
    df = df.rename(columns = {"public_nam": "Name"})

    df.to_csv("../data/geocoded/bus_geocoded.csv", index = False)

    return df