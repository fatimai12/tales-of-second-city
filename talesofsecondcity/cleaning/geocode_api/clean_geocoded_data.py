"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Clean data that's been geocoded to use in index

"""
import pandas as pd
import re

def clean_parks():
    """
    Clean parks data
    """
    parks = pd.read_csv("../../data/transformed/parks_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    parks = parks[["ID", "Tract"]]

    # Remove the ".0" from the end of the tract column
    parks = parks.replace(to_replace = r'\.0$', value = "", regex = True)

    # Put leading zeros back in
    parks["Tract"] = parks["Tract"].str.zfill(6)

    # Drop parks that could not be geocoded (n = 2)
    parks = parks.drop(parks[parks["Tract"].isnull()].index)
    parks.to_csv("../../data/transformed/parks_final.csv", index = False)

def clean_libraries():
    """
    Clean libraries data
    """
    # Read in geocoded libraries data
    libraries = pd.read_csv("../../data/transformed/libraries_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    libraries = libraries[["id", "tract"]]
    # Put leading zeros back in
    libraries["tract"] = libraries["tract"].str.zfill(6)

    # Rename columns to be consistent across all data
    libraries = libraries.rename(columns = {"id": "ID", "tract": "Tract"})
    libraries.to_csv("../../data/transformed/libraries_final.csv", index = False)

clean_parks()
clean_libraries() 

