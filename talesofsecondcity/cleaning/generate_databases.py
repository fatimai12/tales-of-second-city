"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck and Fatima Irfan

Generate final database with all public service and census data
"""
import pandas as pd
from geocode_api import address_to_census_tract
from geocode_api import address_to_census_tract
from geocode_api.point_to_census_tract import geocode_missing_tracts, geocode_l_stops, find_lat_lon
from geocode_api.preprocess_data import preprocess
from geocode_api.clean_geocoded_data import clean_libraries, clean_parks, clean_l_stops, clean_divvy, clean_bus
from ..analysis import index
from census_api import census_scrape

preprocess()
address_to_census_tract.run()
l_stops_geocoded = geocode_l_stops()

#loops? or fine
parks_with_missing = pd.read_csv("../data/geocoded/parks_geocoded.csv", index_col = False)
bus_with_missing = pd.read_csv("../data/geocoded/bus_geocoded.csv", index_col = False)
divvy_with_missing = pd.read_csv("../data/geocoded/divvy_geocoded.csv", index_col = False)

parks_geocoded = geocode_missing_tracts(parks_with_missing, True)
bus_geocoded = geocode_missing_tracts(bus_with_missing, False)
divvy_geocoded = geocode_missing_tracts(divvy_with_missing, False)

#can use dict/mapping for cleaning???
clean_parks(parks_geocoded)
clean_libraries()
clean_l_stops(l_stops_geocoded)
clean_divvy(divvy_geocoded)
clean_bus(bus_geocoded)

#generate index file
index.run()

#generate demographics file
census_scrape.merge_dfs()




