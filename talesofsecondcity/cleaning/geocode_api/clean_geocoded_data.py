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
    Clean parks data
    """
    # parks = pd.read_csv("../data/geocoded/parks_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    df = df[["ID", "Tract"]]

    # Remove the ".0" from the end of the tract column
    df = df.replace(to_replace = r'\.0$', value = "", regex = True)

    # Put leading zeros back in
    df["Tract"] = df["Tract"].str.zfill(6)

    # Drop parks that could not be geocoded (n = 2)
    df = df.drop(df[df["Tract"].isnull()].index)
    df.to_csv("../data/geocoded/parks_geocoded.csv", index = False)

def clean_libraries():
    """
    Clean libraries data
    """
    # Read in geocoded libraries data
    libraries = pd.read_csv("../data/geocoded/libraries_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    libraries = libraries[["id", "tract"]]
    # Put leading zeros back in
    libraries["tract"] = libraries["tract"].str.zfill(6)

    # Rename columns to be consistent across all data
    libraries = libraries.rename(columns = {"id": "ID", "tract": "Tract"})
    libraries.to_csv("../data/geocoded/libraries_geocoded.csv", index = False)

def clean_l_stops(df):
    """
    Clean L stops data
    """
    #### check to drop cols after non chicago census tracts id'd

    #Keep only the ID and tract columns
    df = df[["STOP_ID", "tract"]]

    # Rename columns to be consistent across all data
    df = df.rename(columns = {"STOP_ID": "ID", "tract": "Tract"})

    df.to_csv("../data/geocoded/l_stops_geocoded.csv", index = False)

def clean_divvy(df):
    """
    Clean Divvy data
    """
    #### check to drop cols after non chicago census tracts id'd
    
    # Remove the ".0" from the end of the tract column
    df = df.replace(to_replace = r'\.0$', value = "", regex = True)

    # Put leading zeros back in
    df["Tract"] = df["Tract"].str.zfill(6)

    #Keep only the ID and tract columns
    df = df[["station_name", "Tract"]]

    # Rename columns to be consistent across all data
    df = df.rename(columns = {"station_name": "Station Name"})

    df.to_csv("../data/geocoded/divvy_geocoded.csv", index = False)

def clean_bus(df):
    """
    Clean bus data
    """
    #### check to drop cols after non chicago census tracts id'd

    #Keep only the ID and tract columns
    df = df[["public_nam", "Tract"]]

    # Rename columns to be consistent across all data
    df = df.rename(columns = {"public_nam": "Public Name", "tractce10": "Tract"})

    df.to_csv("../data/geocoded/bus_geocoded.csv", index = False)