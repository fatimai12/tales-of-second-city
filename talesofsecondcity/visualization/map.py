import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt

# shapefile_path = "../data/original/tl_2022_17_tract.shp"
shapefile_path = "talesofsecondcity/data/original/Boundaries - Census Tracts - 2010.geojson"
gdf = gpd.read_file(shapefile_path)
gdf.plot()
plt.show()