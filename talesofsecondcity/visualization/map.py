import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pygris import tracts, counties
from pygris.utils import shift_geometry
from pygris.data import get_census

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



chicago_tracts_cartographic_21 = tracts(state = "IL", county = "Cook", cb = True, cache = True, year = 2021)
chicago_tracts_cartographic_20 = tracts(state = "IL", county = "Cook", cb = True, cache = True, year = 2020)


# Plot the two side-by-side to compare them
fig, ax = plt.subplots(ncols = 2)

chicago_tracts_cartographic_21.plot(ax = ax[0])
chicago_tracts_cartographic_20.plot(ax = ax[1])


ax[0].set_title("TIGER/Line")
ax[1].set_title("Cartographic")

https://walker-data.com/pygris/03-data-utilities/

us_youth_sahie = get_census(dataset = "timeseries/healthins/sahie",
                            variables = "PCTUI_PT",
                            params = {
                                "for": "county:*",
                                "in": "state:*",
                                "time": 2019,
                                "AGECAT": 4
                            }, 
                            return_geoid = True, 
                            guess_dtypes = True)

us_counties = counties(cb = True, resolution = "20m", cache = True, year = 2019)
us_counties_rescaled = shift_geometry(us_counties)

us_counties_merged = us_counties_rescaled.merge(us_youth_sahie, on = "GEOID")

us_counties_merged.plot(
    column = "PCTUI_PT",
    cmap = "viridis",
    figsize = (8, 6)
)

plt.title("% uninsured under age 19 by county, 2019")
