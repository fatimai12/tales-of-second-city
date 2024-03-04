"""
CAPP 30122
Team: Tales of Second City
Author: Suchi Tailor and Fatima Irfan

Create a map visualization based on acs5 demographics 

https://towardsdatascience.com/creating-choropleth-maps-with-pythons-folium-library-cfacfb40f56a
"""
import geopandas as gpd
import folium
import pandas as pd
import plotly.express as px

all_census_tracts = gpd.read_file("talesofsecondcity/data/geocoded/tiger_22_final.geojson")
all_census_tracts = all_census_tracts.to_crs("EPSG:4326")
city_boundaries = gpd.read_file('talesofsecondcity/data/original/Boundaries - City.geojson')
city_census_tracts = gpd.overlay(all_census_tracts, city_boundaries, how = "intersection")
full_demo = gpd.read_file("talesofsecondcity/data/full_demo_data.geojson")
city_full_demo = gpd.overlay(full_demo, city_boundaries, how = "intersection")

lat=41.8227
long=-87.6014

def display_index_choropleth():
    df = pd.read_csv('talesofsecondcity/data/index_data.csv',dtype=str)
    df['APS Index'] = pd.to_numeric(df['APS Index'])

    fig = px.choropleth(
        data_frame = df,
        geojson = city_census_tracts,
        featureidkey = 'properties.tract',
        locations = 'Tract',
        color = 'APS Index',
        color_continuous_scale = 'viridis',
        scope = 'usa',
        center = dict(lat = lat, lon = long),
        basemap_visible = False)

    fig.update_layout(autosize = True, geo = dict(projection_scale = 70),
                      margin=dict(t=0, b=0, l=0, r=0))

    return fig

def display_change_over_time_choropleth():
    lat=41.8227
    long=-87.6014

    df = pd.read_csv('talesofsecondcity/data/full_demo_data.csv')
    df.drop(columns=['NAME_x','Name','NAMELSAD','MTFCC','FUNCSTAT'],inplace=True)
    df.iloc[:, ~df.columns.str.contains('geometry')] = df.iloc[:, ~df.columns.str.contains('geometry')].apply(pd.to_numeric)
    df['change_in_pct_white_2012_to_2022'] = (
        (df['Race: White_2012']/df['Total Pop (#)_2012']) - 
        (df['Race: White_2022']/df['Total Pop (#)_2022'])
        ) * 100

    fig = px.choropleth(
        data_frame = df,
        geojson = city_census_tracts,
        featureidkey = 'properties.tract',
        locations = 'tract',
        color = 'change_in_pct_white_2012_to_2022',
        color_continuous_scale = 'viridis',
        scope = 'usa',
        center = dict(lat = lat, lon = long),
        basemap_visible = False)

    fig.update_layout(autosize = True, geo = dict(projection_scale = 70),
                      margin=dict(t=0, b=0, l=0, r=0))

    return fig


def display_demo_chloropleth(col):

    # load geojson files
    tiger_12 = gpd.read_file('talesofsecondcity/data/geocoded/tiger_12_final.geojson')
    tiger_17 = gpd.read_file('talesofsecondcity/data/geocoded/tiger_17_final.geojson')
    tiger_22 = gpd.read_file('talesofsecondcity/data/geocoded/tiger_22_final.geojson')
    city_boundaries = gpd.read_file('talesofsecondcity/data/original/Boundaries - City.geojson')
    neighborhoods = gpd.read_file('talesofsecondcity/data/original/Boundaries - Neighborhoods.geojson')

    #generate map & base layers
    base_map = folium.Map(location=[41.7377, -87.6976], zoom_start=11, overlay = False, name = "base")
    folium.GeoJson(city_boundaries, name = "city boundaries", fill = False, color = "black").add_to(base_map)
    folium.GeoJson(neighborhoods, name = "Neigborhood Boundaries", 
               zoom_on_click= True,
               fill = False,     
                style_function=lambda feature: {
                    # "fillColor": "#ffff00",
                    "color": "maroon",
                    "weight": 3,
                    "dashArray": "5, 5",
                },
            ).add_to(base_map)

    # develop Choropleth maps
    # map_12 = folium.Choropleth(
    #     geo_data=tiger_12,
    #     name="2008-2012 ACS 5-year Estimates",
    #     data=tiger_12,
    #     columns= ["GEOID", col],
    #     key_on= "feature.properties.GEOID",
    #     fill_color= "YlGn",
    #     fill_opacity= 0.7,
    #     line_opacity= 0.2,
    #     highlight = True, 
    #     line_color = 'black',
    #     overlay = True,
    #     legend_name= "2008-2012 ACS 5-year Estimates").add_to(base_map)
    
    map_12 = folium.Choropleth(
        geo_data=city_full_demo,
        name="2008-2012 ACS 5-year Estimates",
        data=city_full_demo,
        columns= ["GEOID_x", 'Race: White_2012'],
        key_on= "feature.properties.GEOID_x",
        fill_color= "YlGn",
        fill_opacity= 0.7,
        line_opacity= 0.2,
        highlight = True,
        line_color = 'black',
        overlay = True,
        nan_fill_color = 'Grey',
        legend_name= "2008-2012 ACS 5-year Estimates").add_to(base_map)
    
    map_17 = folium.Choropleth(
        geo_data=tiger_17,
        name="2013-2017 ACS 5-year Estimates",
        data=tiger_17,
        columns= ["GEOID", col],
        key_on="feature.properties.GEOID",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight = False,
        overlay = True,
        nan_fill_color = 'Grey',
        line_color = 'black',
        legend_name="2013-2017 ACS 5-year Estimates").add_to(base_map)

    map_22 = folium.Choropleth(
        geo_data=tiger_22,
        name="2018-2022 ACS 5-year Estimates",
        data=tiger_22,
        columns= ["GEOID", col],
        key_on="feature.properties.GEOID",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight = False,
        overlay = True,
        nan_fill_color = 'Grey',
        line_color = 'black',
        legend_name="2018-2022 ACS 5-year Estimates").add_to(base_map)
        
    # Add Customized Tooltips to each map layer
    folium.features.GeoJson(
        data=tiger_12,
        name='2008 - 2012 Population Features',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Home: Owner',
                    'Home: Renter',
                    'Median HH Income ($)',
                    'Edu: HS, no diploma',
                    ],
            aliases=["Home Owners (%):",
                        "Home Renters (%):",
                        "Median HH Income ($)",
                        "No HS Diploma (%)",
                    ], 
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,),
                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
            ).add_to(map_12)  

    folium.features.GeoJson(
        data= tiger_17,
        name='2017-2022 Population Features',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Home: Owner',
                    'Home: Renter',
                    'Median HH Income ($)',
                    'Edu: HS, no diploma',
                    ],
            aliases=["Home Owners (%):",
                        "Home Renters (%):",
                        "Median HH Income ($)",
                        "No HS Diploma (%)",
                    ], 
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,),
                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
            ).add_to(map_17)   
    
    folium.features.GeoJson(
        data=tiger_22,
        name='2022 Population Features',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Home: Owner',
                    'Home: Renter',
                    'Median HH Income ($)',
                    'Edu: HS, no diploma',
                    ],
            aliases=["Home Owners (%):",
                        "Home Renters (%):",
                        "Median HH Income ($)",
                        "No HS Diploma (%)",
                    ], 
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,),
                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
            ).add_to(map_22)  
    
    folium.LayerControl().add_to(base_map)

    base_map.save("layer_map.html")
    
    return open("layer_map.html", 'r').read()

    # return base_map