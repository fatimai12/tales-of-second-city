"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Clean parks and libraries data for use in geocode api
"""

import pandas as pd

def preprocess():
    """
    Read in parks and libraries data and clean. Exclude rows without addresses.

    Returns:
        None, saves dataframes as cleaned CSVs
    """

    parks = pd.read_csv("../data/original/CPD_Parks.csv", dtype = str, 
                        skipinitialspace = True)
    libraries = pd.read_csv("../data/original/libraries.csv", dtype = str,
                            skipinitialspace = True)

    # Clean data
    parks = parks[["PARK_NO", "LOCATION", "ZIP", "PARK"]]
    # Drop row that does not have an address (bike trail)
    parks = parks.drop(parks[parks["LOCATION"].isnull()].index)
    parks.insert(2, "CITY", "Chicago")
    parks.insert(3, "STATE", "IL")
    parks.to_csv("../data/preprocessed/parks_clean.csv", index = False)

    libraries = libraries[["NAME", "ADDRESS", "CITY", "STATE", "ZIP"]]
    libraries.to_csv("../data/preprocessed/libraries_clean.csv", index = False)