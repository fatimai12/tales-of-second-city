"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Clean parks data for use in geocode api


"""
import pandas as pd

parks = pd.read_csv("talesofsecondcity/data/original/CPD_Parks.csv", dtype = str)
libraries = pd.read_csv("talesofsecondcity/data/original/libraries.csv", dtype = str)

# Clean data
parks = parks[["PARK_NO", "LOCATION", "ZIP"]]
parks.insert(2, "CITY", "Chicago")
parks.insert(3, "STATE", "IL")
parks.to_csv("talesofsecondcity/data/transformed/parks_clean.csv", index = False)

libraries = libraries[["NAME", "ADDRESS", "CITY", "STATE", "ZIP"]]
libraries.to_csv("talesofsecondcity/data/transformed/libraries_clean.csv", index = False)