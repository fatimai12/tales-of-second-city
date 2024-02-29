from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
MAP_BOX_TOKEN = "pk.eyJ1IjoiZmlyZmFuIiwiYSI6ImNsdDZxaTB3bDBkZnUycXQzOHAzejBpcW8ifQ.QLZRJ_SQfPxO2rxZAUzGnw"
px.set_mapbox_access_token("MAP_BOX_TOKEN")

# from visualization.map import gen_index_choropleth

app = Dash(__name__)
# index_map = gen_index_choropleth()

df = pd.read_csv('data/indexed_data.csv')
json_df = df.to_dict(orient='records')
census_tracts = gpd.read_file("data/original/Boundaries - Census Tracts - 2010.geojson")
lat=41.8227
long=-87.6014

def gen_index_map():
    fig = px.choropleth_mapbox(
            json_df, 
            geojson = census_tracts, 
            locations = "Tract", 
            featureidkey="properties.tractce10",
            color="Total Score", 
            #color_continuous_scale=custom_reds, 
                range_color=(0, 1), 
            # mapbox_style="carto-positron", opacity=0.6,
            hover_name="Tract",
            center={"lat": lat, "lon": long}
            # zoom=10
            )

    return fig

fig = gen_index_map()

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

# fig = px.choropleth(geo_df,
#                    geojson=geo_df.geometry,
#                    locations=geo_df.index,
#                    color="Joly",
#                    projection="mercator")
# fig.update_geos(fitbounds="locations", visible=False)

# app.layout = dbc.Container([
#     # header
#     dbc.Row([
#         dbc.Col([
#             # html.Br(), 
#             html.H1(children='Hello Dash'), 
#                     # style={'text-align':'center'}),
#             html.Div(children='''
#                 Dash: A web application framework for your data.
#             ''')
#             # style={'text-align':'center'}),
#         # ], width=12) 
#     ], align='end'),
    
#     # index map
#     dbc.Row([
#         dbc.Col([

#             html.H3('Public Service Access by Census Tract', 
#             style={'text-align':'center'}),
            
#             dcc.Graph(
#                 id='map-idx',
#                 figure = fig)
#         ], width=12)
#     ], align='center')
#     ])
# ])


# # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# # app.layout = html.Div([
# #     dcc.Graph(id='graph-with-slider'),
# #     dcc.Slider(
# #         df['year'].min(),
# #         df['year'].max(),
# #         step=None,
# #         value=df['year'].min(),
# #         marks={str(year): str(year) for year in df['year'].unique()},
# #         id='year-slider'
# #     )
# # ])

# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'))

# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]

#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                      size="pop", color="continent", hover_name="country",
#                      log_x=True, size_max=55)

#     return fig

# def update_output(n_clicks, value):
#     return f'The input value was "{value}" and the button has been clicked {n_clicks} times.'

# #layout
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


# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")