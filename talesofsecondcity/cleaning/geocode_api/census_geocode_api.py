"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Use Census Geocode API nad pygris package to match zipcodes and coordinates
to census tracts

"""
import pandas as pd
from pygris.geocode import geolookup, batch_geocode

parks = pd.read_csv("../../data/original/parks_clean.csv", dtype = str)
libraries = pd.read_csv("../../data/original/libraries_clean.csv", dtype = str)

parks_geocode = batch_geocode(parks, id_column = "PARK_NO",
                          address = "LOCATION", city = "CITY", state = "STATE",
                          zip = "ZIP")
parks_geocode.to_csv("../../data/transformed/parks_geocoded.csv", index = False)

libraries_geocode = batch_geocode(libraries, id_column = "NAME",
                          address = "ADDRESS", city = "CITY", state = "STATE",
                          zip = "ZIP")
libraries_geocode.to_csv("../../data/transformed/libraries_geocoded.csv", index = False)

