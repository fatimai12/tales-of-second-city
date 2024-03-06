"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck and Fatima Irfan

Map geojson file rows to corresponding census tracts.
Use Census Geocode API and pygris package to match zipcodes and coordinates
to census tracts.

"""
import pandas as pd
import geopandas as gpd
from pygris.geocode import geolookup, batch_geocode
from geopy.geocoders import Nominatim
import time

def run():
    """
    Assigns geocodes/census tracts to original or preprocessed
    data with address and/or point information.
    """

    # Batch geocode as many locations as possible
    census_tracts = gpd.read_file("../data/original/Boundaries - Census Tracts - 2010.geojson")

    parks = pd.read_csv("../data/preprocessed/parks_clean.csv", dtype = str)
    libraries = pd.read_csv("../data/preprocessed/libraries_clean.csv", dtype = str)

    parks_geocode = batch_geocode(parks, id_column = "PARK_NO",
                            address = "LOCATION", city = "CITY", state = "STATE",
                            zip = "ZIP")

    libraries_geocode = batch_geocode(libraries, id_column = "NAME",
                            address = "ADDRESS", city = "CITY", state = "STATE",
                            zip = "ZIP")

    libraries_geocode.to_csv("../data/geocoded/libraries_geocoded.csv", index = False)

    #Assign census tracts to bus stops and divvy using spatial join
    bus_stops = gpd.read_file("../data/original/CTA Bus Stops.geojson")
    bus_geocode = gpd.sjoin(bus_stops, census_tracts, how="left", predicate="within")
    bus_geocode = bus_geocode[["public_nam","geometry", "tractce10"]]
    bus_geocode['longitude'] = bus_geocode.geometry.x
    bus_geocode['latitude'] = bus_geocode.geometry.y

    divvy_stations = gpd.read_file("../data/original/Divvy Bicycle Stations.geojson")
    divvy_geocode = gpd.sjoin(divvy_stations, census_tracts, how="left", predicate="within")
    divvy_geocode = divvy_geocode[["station_name","latitude", "longitude", "tractce10"]]

    # Clean up formatting to find tracts that are missing after batch geocoding
    parks_geocode['latlong'] = parks_geocode['latitude'].astype(str) + '_' + parks_geocode['longitude'].astype(str)
    parks_geocode = pd.merge(parks, parks_geocode, on="Common Identifier", how="left")

    #Rename columns for ease of processing
    parks_geocode = parks_geocode.rename(columns = {"id": "ID", "tract": "Tract"})
    bus_geocode = bus_geocode.rename(columns = {"tractce10": "Tract"})
    divvy_geocode = divvy_geocode.rename(columns = {"tractce10": "Tract"})

    #Output (partially) geocoded files
    parks_geocode.to_csv("../data/geocoded/parks_geocoded.csv", index = False)
    bus_geocode.to_csv("../data/geocoded/bus_geocoded.csv", index = False)
    divvy_geocode.to_csv("../data/geocoded/divvy_geocoded.csv", index = False)


