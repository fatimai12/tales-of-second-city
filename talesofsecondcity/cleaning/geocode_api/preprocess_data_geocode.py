"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Clean parks data for use in geocode api


"""
import pandas as pd

parks = pd.read_csv("../data/original/CPD_Parks.csv", dtype = str, 
                    skipinitialspace = True)
libraries = pd.read_csv("../data/original/libraries.csv", dtype = str,
                        skipinitialspace = True)

# Clean data
parks = parks[["PARK_NO", "LOCATION", "ZIP"]]
# Drop row that does not have an address (bike trail)
parks = parks.drop(parks[parks["LOCATION"].isnull()].index)
parks.insert(2, "CITY", "Chicago")
parks.insert(3, "STATE", "IL")
parks.to_csv("../data/cleaned/parks_clean.csv", index = False)

libraries = libraries[["NAME", "ADDRESS", "CITY", "STATE", "ZIP"]]
libraries.to_csv("../data/cleaned/libraries_clean.csv", index = False)