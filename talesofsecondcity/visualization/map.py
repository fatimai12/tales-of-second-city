import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pygris import tracts, counties
from pygris.utils import shift_geometry
from pygris.data import get_census

#fatima's work
# shapefile_path = "../data/original/tl_2022_17_tract.shp"
census_shapefile_path = "talesofsecondcity/data/original/Boundaries - Census Tracts - 2010.geojson"
city_shapefile_path = "talesofsecondcity/data/original/Boundaries - City.geojson"

census_map = gpd.read_file(census_shapefile_path)
city_map = gpd.read_file(city_shapefile_path)
fig, ax = plt.subplots(ncols = 2)
census_map.plot(ax = ax[0])
city_map.plot(ax = ax[1])
ax[0].set_title("Census tracts")
ax[1].set_title("City boundary")
plt.show()

tracts_cartographic_21 = tracts(state = "IL", county = "Cook", cb = True, cache = True, year = 2021)
tracts_cartographic_20 = tracts(state = "IL", county = "Cook", cb = True, cache = True, year = 2020)
fig, ax = plt.subplots(ncols = 2)
tracts_cartographic_21.plot(ax = ax[0])
tracts_cartographic_20.plot(ax = ax[1])
ax[0].set_title("Tracts 2021")
ax[1].set_title("Tracts 2020")
plt.show()


# Plot the city boundaries
ax = city_map.plot(color='none', edgecolor='black')

# Plot the census tracts on top of the city boundaries
census_map.plot(ax=ax, color='red', alpha=0.5)

# Show the plot
plt.show()

#https://walker-data.com/pygris/03-data-utilities/

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
