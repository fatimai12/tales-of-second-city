"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck and Fatima Irfan

Generate final database with all public service and census data
"""
import pandas as pd
# from .geocode_api.point_to_census_tract import geocode_l_stops
from geocode_api import point_to_census_tract

l_stops_geocode = point_to_census_tract.geocode_l_stops()

address_to_census_tract.run()

#loops? or fine
parks_with_missing = pd.read_csv("../../data/geocoded/parks_geocoded.csv", index = False)
bus_with_missing = pd.read_csv("../../data/geocoded/bus_geocoded.csv", index = False)
divvy_with_missing = pd.read_csv("../../data/geocoded/divvy_geocoded.csv", index = False)

parks_geocode = geocode_missing_tracts(parks_with_missing, find_lat_long = True)
bus_geocode = geocode_missing_tracts(bus_with_missing, find_lat_long = False)
divvy_geocode = geocode_missing_tracts(divvy_with_missing, find_lat_long = False)

l_stops_geocode.to_csv("../data/geocoded/l_stops_geocoded.csv", index = False)
parks_geocode.to_csv("../../data/geocoded/parks_geocoded.csv", index = False)
divvy_geocode.to_csv("../../data/geocoded/divvy_geocoded.csv", index = False)
bus_geocode.to_csv("../../data/geocoded/bus_geocoded.csv", index = False)

# add cleaning/column dropping for other data files
#can use dict/mapping??

def clean_parks():
    """
    Clean parks data
    """
    parks = pd.read_csv("../../data/geocoded/parks_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    parks = parks[["ID", "Tract"]]

    # Remove the ".0" from the end of the tract column
    parks = parks.replace(to_replace = r'\.0$', value = "", regex = True)

    # Put leading zeros back in
    parks["Tract"] = parks["Tract"].str.zfill(6)

    # Drop parks that could not be geocoded (n = 2)
    parks = parks.drop(parks[parks["Tract"].isnull()].index)
    # parks.to_csv("../../data/geocoded/parks_final.csv", index = False)

def clean_libraries():
    """
    Clean libraries data
    """
    # Read in geocoded libraries data
    libraries = pd.read_csv("../../data/geocoded/libraries_geocoded.csv", dtype = str)

    # Keep only the ID and tract columns
    libraries = libraries[["id", "tract"]]
    # Put leading zeros back in
    libraries["tract"] = libraries["tract"].str.zfill(6)

    # Rename columns to be consistent across all data
    libraries = libraries.rename(columns = {"id": "ID", "tract": "Tract"})
    # libraries.to_csv("../../data/geocoded/libraries_final.csv", index = False)

clean_parks()
clean_libraries() 

#any ACS cleaning??
#read in ACS files here and
#NOW we can join all into a great big db

