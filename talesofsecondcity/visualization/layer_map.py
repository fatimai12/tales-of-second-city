"""
CAPP 30122
Team: Tales of Second City
Author: Suchi Tailor

Create a map visualization based on acs5 demographics 

https://towardsdatascience.com/creating-choropleth-maps-with-pythons-folium-library-cfacfb40f56a
"""
import geopandas as gpd
import folium

def display_demo_chloropleth():

    # load geojson files
    tiger_12 = gpd.read_file('../data/original/tiger_12_final.geojson')
    tiger_17 = gpd.read_file('../data/original/tiger_17_final.geojson')
    tiger_22 = gpd.read_file('../data/original/tiger_22_final.geojson')
    city_boundaries = gpd.read_file('../data/original/Boundaries - City.geojson')
    neighborhoods = gpd.read_file('../data/original/Boundaries - Neighborhoods.geojson')

    # drop census tracts outside of city boundaries
    tiger_12 = tiger_12.to_crs("EPSG:4326")
    tiger_17 = tiger_17.to_crs("EPSG:4326")
    tiger_22 = tiger_22.to_crs("EPSG:4326")

    tiger_12 = gpd.overlay(tiger_12, city_boundaries, how = "intersection")
    tiger_17 = gpd.overlay(tiger_17, city_boundaries, how = "intersection")
    tiger_22 = gpd.overlay(tiger_22, city_boundaries, how = "intersection")

    #generate map & base layers
    base_map = folium.Map(location=[41.7377, -87.6976], zoom_start=11, overlay = False, name = "base")
    # folium.GeoJson(city_boundaries, name = "City Boundaries").add_to(base_map)
    folium.GeoJson(neighborhoods, name = "Neigborhood Boundaries").add_to(base_map)

    # develop Choropleth maps
    map_12 = folium.Choropleth(
        geo_data=tiger_12,
        name="Population: 2008-2012 ACS 5-year Estimates",
        data=tiger_12,
        columns= ["GEOID","Total Pop (#)"],
        key_on= "feature.properties.GEOID",
        fill_color= "YlGn",
        fill_opacity= 0.7,
        line_opacity= 0.2,
        highlight = True, 
        line_color = 'black',
        overlay = True,
        legend_name= "Population: 2008-2012 ACS 5-year Estimates").add_to(base_map)
    
    map_17 = folium.Choropleth(
        geo_data=tiger_17,
        name="Population: 2013-2017 ACS 5-year Estimates",
        data=tiger_17,
        columns= ["GEOID","Total Pop (#)"],
        key_on="feature.properties.GEOID",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight = False,
        overlay = True,
        line_color = 'black',
        legend_name="Population: 2013-2017 ACS 5-year Estimates").add_to(base_map)

    map_22 = folium.Choropleth(
        geo_data=tiger_22,
        name="Population: 2018-2022 ACS 5-year Estimates",
        data=tiger_12,
        columns= ["GEOID","Total Pop (#)"],
        key_on="feature.properties.GEOID",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight = False,
        overlay = True,
        line_color = 'black',
        legend_name="Population: 2018-2022 ACS 5-year Estimates").add_to(base_map)
        
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

    return base_map