import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# shapefile_path = "../data/original/tl_2022_17_tract.shp"
shapefile_path = "talesofsecondcity/data/original/Boundaries - Census Tracts - 2010.geojson"
gdf = gpd.read_file(shapefile_path)
gdf.plot()
gdf.plot()


# Census tracts for 2022 data 
acs5_2022 = pd.read_csv('../data/original/acs5_data_2022.csv')

#convert codes to strings to create GEOID
acs5_2022["State code"] = acs5_2022["State code"].astype(str)
acs5_2022["County code"] = acs5_2022["County code"].astype(str)
acs5_2022["Tract Code"] = acs5_2022["Tract Code"].astype(str)
acs5_2022["GEOID"] = acs5_2022["State code"] + acs5_2022["County code"] + acs5_2022["Tract Code"]

il_tracts = gpd.read_file('cb_2022_17_tract_500k.zip')
chi_tracts = il_tracts[il_tracts['COUNTYFP'] == '031']

#this merge doesnt actually work that well 
chi_map = (chi_tracts.merge(acs5_2022, how = 'left', left_on = 'GEOID', right_on = 'GEOID'))
