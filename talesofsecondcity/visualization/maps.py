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

city_boundaries = gpd.read_file('talesofsecondcity/data/original/Boundaries - City.geojson')
demo_geojson = gpd.read_file("talesofsecondcity/data/full_demo_data.geojson",dtype="str")
demo_geojson_city = gpd.overlay(demo_geojson, city_boundaries, how = "intersection")
columns_to_convert = demo_geojson_city.columns[13:77]
demo_geojson_city[columns_to_convert] = demo_geojson_city[columns_to_convert].apply(pd.to_numeric, errors='coerce')
neighborhoods = gpd.read_file('talesofsecondcity/data/original/Boundaries - Neighborhoods.geojson')

lat=41.8227
long=-87.6014

def display_index_choropleth():
    df = pd.read_csv('talesofsecondcity/data/index_data.csv',dtype=str)
    df['APS Index'] = pd.to_numeric(df['APS Index'])

    fig = px.choropleth(
        data_frame = df,
        geojson = demo_geojson_city,
        featureidkey = 'properties.TRACTCE',
        locations = 'Tract',
        color = 'APS Index',
        color_continuous_scale = 'viridis',
        scope = 'usa',
        center = dict(lat = lat, lon = long),
        basemap_visible = False,
        title = 'Public Service Access by Census Tract')

    fig.update_layout(autosize = True, geo = dict(projection_scale = 70),
                      margin = dict(t=0, b=0, l=0, r=0),
                      coloraxis_colorbar=dict(
                          len=0.8,
                          yanchor='top',
                          y = 0.9,
                          ypad = 0,
                          thickness=10,
                          xref = "container",
                          yref = "container",
                          orientation = "h"
                    ))

    return fig

def display_change_over_time_choropleth(factor):
    df = pd.read_csv('talesofsecondcity/data/full_demo_data.csv')
    df.drop(columns=['NAME_x','Name','NAMELSAD','MTFCC','FUNCSTAT'],inplace=True)
    df.iloc[:, ~df.columns.str.contains('geometry')] = df.iloc[:, ~df.columns.str.contains('geometry')].apply(pd.to_numeric)
    factor_2022 = factor + "_2022"
    factor_2012 = factor + "_2012"
    new_var = "% Change in " + factor
    df[new_var] = (
        (df[factor_2022]/df['Total Pop (#)_2022']) - 
        (df[factor_2012]/df['Total Pop (#)_2012'])
        ) * 100

    fig = px.choropleth(
        data_frame = df,
        geojson = demo_geojson_city,
        featureidkey = 'properties.TRACTCE',
        locations = 'tract',
        color = new_var,
        range_color = (-max(abs(df[new_var])), 
                       max(abs(df[new_var]))),
        color_continuous_scale = 'viridis',
        scope = 'usa',
        center = dict(lat = lat, lon = long),
        basemap_visible = False,
        title = 'Demographic Factor % Change (from 2017 to 2022)')

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(autosize = True, geo = dict(projection_scale = 70),
                      margin=dict(t=0, b=0, l=0, r=0),
                      coloraxis_colorbar=dict(
                          len=0.8,
                          xpad=0.5,
                          yanchor='top',
                          y = 0.9,
                          ypad = 0,
                          thickness=10,
                          xref = "container",
                          yref = "container",
                          orientation = "h"
                    ))
    return fig


def display_demo_chloropleth(col):

    #generate map & base layers
    base_map = folium.Map(location=[lat, long], zoom_start=11, overlay = False, name = "base")
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

    map_12 = folium.Choropleth(
        geo_data=demo_geojson_city,
        name="2008-2012 ACS 5-year Estimates",
        data=demo_geojson_city,
        columns= ["GEOID", col + '_2012'],
        key_on= "feature.properties.GEOID",
        fill_color= "YlGn",
        fill_opacity= 0.7,
        line_opacity= 0.2,
        highlight = True,
        line_color = 'black',
        overlay = True,
        nan_fill_color = 'Grey',
        legend_name= "2008-2012 ACS 5-year Estimates of " + col).add_to(base_map)
    
    map_17 = folium.Choropleth(
        geo_data=demo_geojson_city,
        name="2013-2017 ACS 5-year Estimates",
        data=demo_geojson_city,
        columns= ["GEOID", col + '_2017'],
        key_on="feature.properties.GEOID",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight = False,
        overlay = True,
        nan_fill_color = 'Grey',
        line_color = 'black',
        legend_name="2013-2017 ACS 5-year Estimates of " + col).add_to(base_map)

    map_22 = folium.Choropleth(
        geo_data=demo_geojson_city,
        name="2018-2022 ACS 5-year Estimates",
        data=demo_geojson_city,
        columns= ["GEOID", col + '_2022'],
        key_on="feature.properties.GEOID",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight = False,
        overlay = True,
        nan_fill_color = 'Grey',
        line_color = 'black',
        legend_name="2018-2022 ACS 5-year Estimates of " + col).add_to(base_map)

    # Add Customized Tooltips to each map layer
    folium.features.GeoJson(
        data=demo_geojson_city,
        name='2008 - 2012 Population Features',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=[col + "_2012"],
            aliases=[col], 
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
        data= demo_geojson_city,
        name='2013-2017 Population Features',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=[col + "_2017"],
            aliases=[col], 
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
        data=demo_geojson_city,
        name='2018-2022 Population Features',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=[col + "_2022"],
            aliases=[
                    # "Total Population (#):",
                     col
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
    
    folium.LayerControl(position = 'topright',collapsed=False).add_to(base_map)

    base_map.save("talesofsecondcity/visualization/layer_map.html")
    
    return open("talesofsecondcity/visualization/layer_map.html", 'r').read()


def ps_marker_map():

    # generate base map
    ps_data = gpd.read_file('talesofsecondcity/data/full_ps_data.csv')
    ps_map = folium.Map(location=[41.7377, -87.6976], zoom_start=11, overlay = False, name = "ps_base")

    # COMMENT OUT BELOW LINE WHEN INCLUDING BUS STOPS
    ps_data = ps_data.drop(ps_data[ps_data['service_type'] == 'bus stop'].index)

    # update for map readability
    service_dict = {'bus stop' : 'Bus Stop',
                    'divvy station' : 'Divvy Station', 
                    'l stop': 'L Stop', 
                    'park' : 'Park', 
                    'library' : 'Library'}
    ps_data["service_type"] = ps_data["service_type"].replace(service_dict)

    # include below line if running with bus stops
    # bus_stops = folium.FeatureGroup("Bus Stops").add_to(ps_map)
    divvy_stations = folium.FeatureGroup("Divvy Bike Stations").add_to(ps_map)
    l_stops = folium.FeatureGroup("L Stop").add_to(ps_map)
    parks = folium.FeatureGroup("Parks").add_to(ps_map)
    library = folium.FeatureGroup("Libraries").add_to(ps_map)

    # Create markers for each location
    feature_dict = {#'Bus Stop' : bus_stops, 
                'Divvy Station' : divvy_stations,
                'L Stop': l_stops, 
                'Park' : parks, 
                'Library' : library
                }
    
    color_dict = {'Bus Stop' : 'red', 
                'Divvy Station' : 'blue',
                'L Stop': 'purple', 
                'Park' : 'darkgreen', 
                'Library' : 'orange'
                }
    
    for _, row in ps_data.iterrows():
        folium.Marker(
            location = [row["latitude"], row["longitude"]],
            tooltip = f'{row["service_type"]} : {row["Name"]}',
            icon= folium.Icon(color = color_dict[row["service_type"]]),
        ).add_to(feature_dict[row["service_type"]])

    folium.LayerControl().add_to(ps_map)

    return ps_map