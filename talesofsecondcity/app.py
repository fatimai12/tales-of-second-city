from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# df = pd.read_csv("data/libraries/libraries.csv")
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))

def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    return fig

def update_output(n_clicks, value):
    return f'The input value was "{value}" and the button has been clicked {n_clicks} times.'

if __name__ == '__main__':
    app.run_server(debug=True)