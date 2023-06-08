

from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

df = px.data.election()  # replace with your own data source

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Montreal 2013 candidate voting pool analysis',
                 className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        html.P("Select a candidate:"),
        dcc.RadioItems(
            id='candidate',
            options=["Joly", "Coderre", "Bergeron"],
            value="Coderre",
            inline=True
        ),

    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=px.histogram(
                df, x='winner', y='total', histfunc='sum'), id='sum-histogram')
        ], width=6),

        dbc.Col([
            dcc.Graph(id="graph"),
        ], width=6),
    ]),

], fluid=True)


@app.callback(
    Output("graph", "figure"),
    Input("candidate", "value"))
def display_choropleth(candidate):
    geojson = px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 6500])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
