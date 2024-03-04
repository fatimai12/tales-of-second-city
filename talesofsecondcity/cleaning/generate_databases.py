"""
CAPP 30122
Team: Tales of Second City
Author: Fatima Irfan

Generate final database with all public service and census data
"""
import pandas as pd
import geopandas as gpd
from geocode_api import address_to_census_tract
from geocode_api import address_to_census_tract
from geocode_api.point_to_census_tract import geocode_missing_tracts, geocode_l_stops
from geocode_api.preprocess_data import preprocess
from geocode_api.clean_geocoded_data import clean_libraries, clean_parks, clean_l_stops, clean_divvy, clean_bus
from .analysis import index
from census_api import census_scrape
from shapely.wkt import loads
import re

preprocess()
address_to_census_tract.run()
l_stops_geocoded = geocode_l_stops()

parks_with_missing = pd.read_csv("../data/geocoded/parks_geocoded.csv", index_col = False)
bus_with_missing = pd.read_csv("../data/geocoded/bus_geocoded.csv", index_col = False)
divvy_with_missing = pd.read_csv("../data/geocoded/divvy_geocoded.csv", index_col = False)

parks_geocoded = geocode_missing_tracts(parks_with_missing, True)
bus_geocoded = geocode_missing_tracts(bus_with_missing, False)
divvy_geocoded = geocode_missing_tracts(divvy_with_missing, False)

parks_final = clean_parks(parks_geocoded)
libraries_final = clean_libraries()
l_stops_final = clean_l_stops(l_stops_geocoded)
divvy_final = clean_divvy(divvy_geocoded)
bus_final = clean_bus(bus_geocoded)

#generate index file
index.run()

#generate full demographics file with shapes
full_acs_data = census_scrape.merge_dfs()
full_acs_data["tract"] = full_acs_data["tract"].astype(str)
census_tract_shapes = gpd.read_file("../data/geocoded/tiger_22_final.geojson")
last_column = census_tract_shapes.iloc[:, -1]  # Select the last column
census_tract_shapes = census_tract_shapes.iloc[:, :12]
census_tract_shapes = pd.concat([census_tract_shapes, last_column], axis=1)

merged_demo = census_tract_shapes.merge(
    full_acs_data, how = "left", right_on = 'tract', left_on = 'TRACTCE'
)
merged_demo = merged_demo.rename(columns = {"NAME_y": "Name"})
merged_demo.replace(-666666666.0, '',inplace=True)
merged_demo = merged_demo[merged_demo['Total Pop (#)_2012'] != 0.0]
merged_demo.to_csv('../data/full_demo_data.csv',index=False)

merged_demo['geometry'] = merged_demo['geometry'].astype(str).apply(loads)
merged_demo_gdf = gpd.GeoDataFrame(merged_demo, geometry='geometry')
merged_demo_gdf.to_file('../data/full_demo_data.geojson',driver='GeoJSON')

#generate public services with lat/long file
ps_with_type = [
    (bus_final, 'bus stop'),
    (divvy_final, 'divvy station'),
    (l_stops_final, 'l stop'),
    (parks_final, 'park'),
    (libraries_final, 'library')
]

combined_df = pd.concat([df.assign(service_type=service_type) for df, service_type in ps_with_type], ignore_index=True)
combined_df.drop(columns=['ID'], inplace=True)
combined_df.to_csv('../data/full_ps_data.csv',index=False)


