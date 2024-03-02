from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import plotly.colors as colors
import matplotlib.pyplot as plt

lat=41.8227
long=-87.6014

app = Dash(__name__)

def display_index_choropleth():
    df = pd.read_csv('data/index_data.csv',dtype=str)
    df['APS Index'] = pd.to_numeric(df['APS Index'])
    census_tracts = gpd.read_file("data/original/Boundaries - Census Tracts - 2010.geojson")

    fig = px.choropleth(
        data_frame = df,
        geojson = census_tracts,
        featureidkey = 'properties.tractce10',
        locations = 'Tract',
        color = 'APS Index',
        color_continuous_scale = 'viridis',
        scope = 'usa',
        center = dict(lat = lat, lon = long),
        basemap_visible = False)

    fig.update_layout(autosize = True, geo = dict(projection_scale = 70))

    return fig

fig_idx = display_index_choropleth()

# app.layout = html.Div([
#     html.H4('Political candidate voting pool analysis'),
#     dcc.Graph(id="fig", figure = fig_idx),
# ])

app.layout = dbc.Container([
    # header
    dbc.Row([
        dbc.Col([
            # html.Br(), 
            html.H1(children='Hello Dash'), 
                    # style={'text-align':'center'}),
            html.Div(children='''
                Dash: A web application framework for your data.
            ''')
            # style={'text-align':'center'}),
        # ], width=12) 
    ], align='end')]),
    
    # index map
    dbc.Row([
        dbc.Col([

            html.H3('Public Service Access by Census Tract', 
            style={'text-align':'center'}),
            
            dcc.Graph(
                id='map-idx',
                figure = fig_idx)
        ], width=12)
    ], align='center')
])

if __name__ == '__main__':
    app.run_server(debug=True)
    
#layout
# NAVBAR = dbc.Navbar(
#     children=[
#         html.A(
#             # Use row and col to control vertical alignment of logo / brand
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         dbc.NavbarBrand("Bank Customer Complaints", className="ml-2")
#                     ),
#                 ],
#             ),
#         )
#     ],
#     color="dark",
#     dark=True,
#     sticky="top",
# )

# BODY = ()

# app.layout = html.Div(children=[NAVBAR, BODY])
