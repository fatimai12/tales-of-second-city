"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Use Census Geocode API and pygris package to match zipcodes and coordinates
to census tracts

"""
import pandas as pd
from pygris.geocode import geolookup, batch_geocode
from geopy.geocoders import Nominatim
import time

parks = pd.read_csv("../../data/original/parks_clean.csv", dtype = str)
libraries = pd.read_csv("../../data/original/libraries_clean.csv", dtype = str)

parks_geocode = batch_geocode(parks, id_column = "PARK_NO",
                          address = "LOCATION", city = "CITY", state = "STATE",
                          zip = "ZIP")


def find_lat_lon(address):
    """
    Find lat and long for missing parks
    """
    geolocator = Nominatim(user_agent = "tales_of_second_city", timeout = 5)

    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None
    

def geocode_missing_parks(parks_data):
    """
    """
    missing_parks_data = parks_data[parks_data["tract"].isnull()]
    for i, row in missing_parks_data.iterrows():
        if find_lat_lon(row["address"]) is None:
            continue
        else:
            latitude, longitude = find_lat_lon(row["address"])
            geocoded_addr = geolookup(longitude = longitude, latitude = latitude, 
                                    geography = "Census Tracts", keep_geo_cols = True)
            tract = str(geocoded_addr["TRACT"].to_string(index = False))
            parks_data.at[i, "tract"] = tract

    return parks_data

parks_geocode = geocode_missing_parks(parks_geocode)

parks_geocode.to_csv("../../data/transformed/parks_geocoded.csv", index = False)


libraries_geocode = batch_geocode(libraries, id_column = "NAME",
                          address = "ADDRESS", city = "CITY", state = "STATE",
                          zip = "ZIP")
libraries_geocode.to_csv("../../data/transformed/libraries_geocoded.csv", index = False)

