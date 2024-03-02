"""
CAPP 30122
Team: Tales of Second City
Author: Suchi Tailor

Code for merging census data to geopanda dataframes using pygris 

https://walker-data.com/pygris/01-basic-usage/
https://walker-data.com/pygris/02-geometries/

"""
import geopandas as gpd
import pandas as pd
from pygris import tracts
from pygris.utils import erase_water

# FIX FILE PATH AS NEEDED!! 
acs5_2012 = pd.read_csv('../../data/original/acs5_data_2012.csv')
acs5_2017 = pd.read_csv('../../data/original/acs5_data_2017.csv')
acs5_2022 = pd.read_csv('../../data/original/acs5_data_2022.csv')

# convert to strings to simplify merge
acs5_2012["tract"] = acs5_2012["tract"].astype(str)
acs5_2017["tract"] = acs5_2017["tract"].astype(str)
acs5_2022["tract"] = acs5_2022["Tract Code"].astype(str)

# loads geometries as geopandas
tracts_tiger_12 = tracts(state = "IL", county = "Cook", cb = False, cache = True, year = 2012)
tracts_tiger_17 = tracts(state = "IL", county = "Cook", cb = False, cache = True, year = 2017)
tracts_tiger_22 = tracts(state = "IL", county = "Cook", cb = False, cache = True, year = 2022)

tiger_12_final = erase_water(tracts_tiger_12)
tiger_17_final = erase_water(tracts_tiger_17)
tiger_22_final = erase_water(tracts_tiger_22)

tiger_12_final = tiger_12_final.merge(acs5_2012, how = 'left', left_on = 'TRACTCE', right_on = 'tract').dropna()
tiger_17_final = tiger_17_final.merge(acs5_2017, how = 'left', left_on = 'TRACTCE', right_on = 'tract').dropna()
tiger_22_final = tiger_22_final.merge(acs5_2022, how = 'left', left_on = 'TRACTCE', right_on = 'tract').dropna()

# tiger_12_final.to_file('../../data/original/tiger_12_final.geojson', driver='GeoJSON')  
# tiger_17_final.to_file('../../data/original/tiger_17_final.geojson', driver='GeoJSON') 
# tiger_22_final.to_file('../../data/original/tiger_22_final.geojson', driver='GeoJSON') 