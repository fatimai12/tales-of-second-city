"""
CAPP 30122
Team: Tales of Second City
Author: Suchi Tailor

https://walker-data.com/pygris/01-basic-usage/
https://walker-data.com/pygris/02-geometries/

"""
import geopandas as gpd
import pandas as pd
from pygris import tracts
from pygris.utils import erase_water
import geojson

def acs_to_geopanda_merge():
    """
    Merge census data to geopanda dataframes using pygris package.

    Outputs: 
        None - saves datasets as geojson files
    """

    # load acs data into pandas dataframe
    acs5_2012 = pd.read_csv('../../data/original/acs5_data_2012.csv')
    acs5_2017 = pd.read_csv('../../data/original/acs5_data_2017.csv')
    acs5_2022 = pd.read_csv('../../data/original/acs5_data_2022.csv')

    # convert to strings to simplify merge
    acs5_2012["tract"] = acs5_2012["tract"].astype(str)
    acs5_2017["tract"] = acs5_2017["tract"].astype(str)
    acs5_2022["tract"] = acs5_2022["Tract Code"].astype(str)

    # loads geometries as geopandas
    tracts_tiger_12 = tracts(state = "IL", county = "Cook", cb = False, 
                             cache = True, year = 2012)
    tracts_tiger_17 = tracts(state = "IL", county = "Cook", cb = False, 
                             cache = True, year = 2017)
    tracts_tiger_22 = tracts(state = "IL", county = "Cook", cb = False, 
                             cache = True, year = 2022)

    tiger_12_waterless = erase_water(tracts_tiger_12)
    tiger_17_waterless = erase_water(tracts_tiger_17)
    tiger_22_waterless = erase_water(tracts_tiger_22)
    
    # merge acs data with census tracts geographies
    tiger_12 = tiger_12_waterless.merge(
        acs5_2012, how = 'left', left_on = 'TRACTCE', right_on = 'tract').dropna()
    tiger_17 = tiger_17_waterless.merge(
        acs5_2017, how = 'left', left_on = 'TRACTCE', right_on = 'tract').dropna()
    
    # get rid of tracts that changed, 44 dropped
    tract_differences = list(set(tiger_22_waterless['TRACTCE']) - set(tiger_12_waterless['TRACTCE']))
    tiger_22_dropped = tiger_22_waterless[~tiger_22_waterless['TRACTCE'].isin(tract_differences)]

    tiger_22 = tiger_22_dropped.merge(
        acs5_2022, how = 'right', left_on = 'TRACTCE', right_on = 'tract').dropna()
    
    # drop census tracts outside of city boundaries
    tiger_12 = tiger_12.set_crs("EPSG:4326")
    tiger_17 = tiger_17.set_crs("EPSG:4326")
    tiger_22 = tiger_22.set_crs("EPSG:4326")

    city_boundaries = gpd.read_file('../../data/original/Boundaries - City.geojson')

    tiger_12_final = gpd.overlay(tiger_12, city_boundaries, how = "intersection")
    tiger_17_final = gpd.overlay(tiger_17, city_boundaries, how = "intersection")
    tiger_22_final = gpd.overlay(tiger_22, city_boundaries, how = "intersection")

    # save files as geojsons to use in visualizations
    tiger_12_final.to_file('../../data/geocoded/tiger_12_final.geojson', 
                           driver='GeoJSON')  
    tiger_17_final.to_file('../../data/geocoded/tiger_17_final.geojson', 
                           driver='GeoJSON') 
    tiger_22_final.to_file('../../data/geocoded/tiger_22_final.geojson', 
                           driver='GeoJSON') 

