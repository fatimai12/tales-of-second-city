"""
CAPP 30122
Team: Tales of Second City
Author: Fatima Irfan and Victoria Beck

Map point data file rows to corresponding census tracts
"""

from geopy.geocoders import Nominatim
import pandas as pd
import geopandas as gpd
from pygris.geocode import geolookup

census_tracts = gpd.read_file("../data/original/Boundaries - Census Tracts - 2010.geojson")
l_stops_df = pd.read_csv("../data/original/CTA_-_System_Information_-_List_of__L__Stops_-_Map.csv")

def geocode_l_stops():
    """
    """
    geolocator = Nominatim(user_agent="talesofsecondcity") 

    for row in l_stops_df.itertuples():
        lat, long = row.Location.strip("()").split(",")
        geocoded_addr = geolookup(longitude = long, latitude = lat, 
                                geography = "Census Tracts", keep_geo_cols = True)
        tract = str(geocoded_addr["TRACT"].to_string(index = False))
        l_stops_df.at[row.Index, "tract"] = tract
    
    return l_stops_df


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
    

def geocode_missing_tracts(df: pd, need_lat_lon: bool):
    """
    Geocode data with missing census tracts
    """

    missing_data = df[df["Tract"].isnull()]
    for i, row in missing_data.iterrows():
        if need_lat_lon:
            if find_lat_lon(row["address"]) is None:
                continue
            else:
                latitude, longitude = find_lat_lon(row["address"])
        else:
            latitude = row["latitude"]
            longitude = row["longitude"]
            geocoded_addr = geolookup(longitude = longitude, latitude = latitude, 
                                    geography = "Census Tracts", keep_geo_cols = True)
            tract = str(geocoded_addr["TRACT"].to_string(index = False))
            df.at[i, "Tract"] = tract

    return df