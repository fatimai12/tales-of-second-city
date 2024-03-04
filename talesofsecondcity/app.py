from dash import Dash, html, dcc, Input, Output, State, dash_table, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import plotly.colors as colors
from dash_bootstrap_templates import load_figure_template

# Import map function
from .visualization.maps import display_demo_chloropleth, display_index_choropleth, display_change_over_time_choropleth

load_figure_template("SOLAR")

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# Index data
index_data = pd.read_csv("talesofsecondcity/data/index_data.csv")

fig_idx = display_index_choropleth()
fig_change = display_change_over_time_choropleth()

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([

                html.Div([
                    html.H1(children = "Tales of Second City", 
                            style = {"textAlign": "center", "color": "#BFD9BF", 
                                     "fontSize": 50,
                                     "marginTop": 20, "marginBottom": 0}),
                    html.H2(children = "Mapping Demographic Change and Access to \
                            Public Services in the City of Chicago", 
                            style = {"textAlign": "center", "color": "#FFEFD5", 
                                     "marginTop": 0}),
                ]),
                html.Div([
                    html.Label("We are interested in visualizing and analyzing access \
                               to public services across Chicago in addition to mapping \
                               demographic change across the city.  We hope to be able to \
                               track socioeconomic changes across census tracts and \
                               determine which areas of the city have the highest \
                               access to public services like libraries, parks, and transit.")
                ], style = {"marginBottom": 20, "fontSize": 20, "color": "#FFFFFF"})
            ])
        
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3(children = "Access to Public Services (APS) Index", 
                        style = {"textAlign": "center", "color": "#FFEFD5", 
                                 "fontSize": 25, "marginBottom": 20})
            ]),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(children="Public Service Scores (out of 100) and APS Index (0 to  1) by Census Tract", 
                     style = {"color": "#FFFFFF", "fontSize": 18}),
            dash_table.DataTable(data = index_data.to_dict("records"),
                                 fixed_columns = {"headers": True, "data": 1},
                                 style_table={"minWidth": '100%'},
                                 page_size = 15,
                                 style_cell = {"backgroundColor": "#FFFAF0", "color": "#2F4F4F"},
                                 style_header = {"backgroundColor": "#BFD9BF", 
                                                 "fontWeight": "bold", "color": "#002633"}
                                )

        ], width = 6),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    index_data.columns.unique()[1:],
                    "Park Acres",
                    id = "xaxis")
                    ], style = {"marginTop": 10, "marginBottom": 10}),
            html.Div([
                dcc.Dropdown(
                    index_data.columns.unique()[1:],
                    "Parks Score",
                    id = "yaxis")
                    ], style = {"marginTop": 10, "marginBottom": 10}),
            dcc.Graph(
                id = "Index graph"
             )
        ], width = 6)
    ]),

    # index map

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Br(),
                html.H3('Public Service Access by Census Tract', 
                style={"text-align":"center","color": "#FFEFD5", "fontSize": 25}),
            
                dcc.Graph(
                    id='map-idx',
                    figure = fig_idx,
                    style = {"width": "100%", "height": "600px"},
                    responsive = True)
            ]), width=8,

    #change over time map
        dbc.Col([

            html.H3('Demographic Factor Change', 
            style={'text-align':'center'}),
            
            dcc.Graph(
                id='map-change',
                figure = fig_change)
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Div([
                html.H3(children = "Distribution of Demographic Factors (2012, 2017, 2022)", 
                        style = {"textAlign":"center", "color": "#FFEFD5", "fontSize": 25})
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(id = "map_variable", 
                    options = [
                    {"label": "Total Population (#)", "value": "Total Pop (#)"},
                    {"label": "Total Households (#)", "value": "Total HH (#)"},
                    {"label": "Homeowners (%)", "value": "Home: Renter"},
                    {"label": "Renters (%)", "value": "Home: Owner"},
                    {"label": "Race: White (%)", "value": "Race: White"},
                    {"label": "Race: Black/African-American (%)", "value": "Race: Black/AA"},
                    {"label": "Race: American Indian/Alaskan (%)", "value": "Race: AI/Alaskan"},
                    {"label": "Race: Asian (%)", "value": "Race: Asian"},
                    {"label": "Race: Hawaiian/Pacific Islander (%)", "value": "Race: Hawaiian/PI"},
                    {"label": "Race: Other (%)", "value": "Race: Other"},
                    {"label": "Ethnicity: Hispanic (%)", "value": "Ethnicty: Hisp."},
                    {"label": "Ethnicity: Non-Hispanic (%)", "value": "Ethnicity: Non-Hisp."},
                    {"label": "Highest level of education: Less than 9th Grade (%)", "value": "Edu: < 9th grade"},
                    {"label": "Highest level of education: High School, No Diploma (%)", "value": "Edu: HS, no diploma"},
                    {"label": "Highest level of education: High School Diploma (%)", "value": "Edu: HS Diploma"},
                    {"label": "Highest level of education: Associate's Degree (%)", "value": "Edu: Associate's Degree"},
                    {"label": "Highest level of education: Bachelor's Degree (%)", "value": "Edu: Bachelor's Degree"},
                    {"label": "Highest level of education: Graduate/Professional Degree (%)", "value": "Edu: Grad/Prof Degree"},
                    {"label": "Median Household Income ($)", "value": "Median HH Income ($)"},
                    {"label": "Age 18+ (%)", "value": "Age: 18+"},
                    {"label": "Age 65+ (%)", "value": "Age: 65+"},
                    ], value = "Total Pop (#)", clearable = False),
            ]),
            html.Br(),
            html.Div([
                html.Iframe(id = "Layer Map", srcDoc = None, width = "100%", height = "600px")
            ])
        ])
    ]),

    #change over time map
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3('Demographic Factor Change', 
                style={'text-align':'center', "color": "#FFEFD5", "fontSize": 25}),
                
                dcc.Graph(
                    id='map-change',
                    figure = fig_change,
                    style = {"width": "100%", "height": "600px"},
                    responsive = True)
            ])
        ], width = 12)
    ], align='center'),

    dbc.Row([
        dbc.Col([
            html.Footer("Victoria Beck, Fatima Irfan, Suchi Tailor, CAPP 122 Winter 2024",
                        style = {"textAlign": "center", "marginTop": 20, "marginBottom": 5})
        ])
    ])



])

@callback(
    Output("Index graph", "figure"),
    Input("xaxis", "value"),
    Input("yaxis", "value")
)

def update_graph(x_axis_name, y_axis_name):
    index_bar_chart = px.scatter(index_data, x = x_axis_name, 
                                 y = y_axis_name, 
                                 color = "APS Index", 
                                 hover_name = "Tract")
    return index_bar_chart

@callback(
    Output("Layer Map", "srcDoc"),
    Input("map_variable", "value")
)

def generate_layer_map(variable_name):
    if not variable_name:
        variable_name = 'Total Pop (#)'
    layer_map = display_demo_chloropleth(variable_name)

    return layer_map

    # return html.Iframe(srcDoc = layer_map, style = {'width': '100%', 'height': '600px'})


if __name__ == '__main__':
    app.run_server(debug=True)
    
