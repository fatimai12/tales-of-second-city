import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path = "../data/original/tl_2022_17_tract.shp"
gdf = gpd.read_file(shapefile_path)
gdf.plot()
gdf.plot()