import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pygris import tracts, counties
from pygris.utils import shift_geometry, erase_water
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

tracts_tiger_12 = tracts(state = "IL", county = "Cook", cb = False, cache = True, year = 2012)
tiger_12_erased = erase_water(tracts_tiger_12)

fig, ax = plt.subplots(ncols = 2)
tracts_tiger_12.plot(ax = ax[0])
tiger_12_erased.plot(ax = ax[1])
ax[0].set_title("2012 With Water")
ax[1].set_title("2012 Without Water ")
plt.show()


# Plot the city boundaries
ax = city_map.plot(color='none', edgecolor='black')

# Plot the census tracts on top of the city boundaries
census_map.plot(ax=ax, color='red', alpha=0.5)

# Show the plot
plt.show()

#https://walker-data.com/pygris/03-data-utilities/

# Census tracts for 2022 data
