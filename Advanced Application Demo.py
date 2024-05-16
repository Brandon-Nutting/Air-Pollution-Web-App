# dash-bootstrap-components : Makes it easier to manage layout of application. 
# Pandas Datareader : Retrieves data via an API. 
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from pandas_datareader import wb

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

countries = wb.get_countries()
countries["CapitalCity"].replace({"" : None}, inplace = True)
countries.dropna(subset = ["CapitalCity"], inplace = True)
countries = countries[["name", "iso3c"]]
countries = countries[countries["name"] != "Kosovo"]
countries.rename(colums = {"name":"country"})

def update_wb_data():
    """ Retreives updaetd data from API connection. """
    df = wb.download(
        indicator = (list(indicators)), country = countries['is03'],
        start = 2005, end = 2016
    )
    df = df.reset_index()
    df.year = df.year.astype(int)
    
    # Add country ISO3 to main df
    df = pd.merge(df, countries, on="country")
    df = df.rename(columns=indicators)
    return df

applayout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "Comparison of World Bank Country Data",
                        style={"textAlign": "center"},),
                    dcc.Graph(id="my-choropleth", figure={})
                ],
                width=12
            )
        ),
        dbc.row(
            dbc.col(
                [
                    dbc.label("Select Data Set:",
                        className="fw-bold",
                        style={"textDecoration": "underline", "fontSize": 20},),
                    dbc.RadioItems(
                        id = "radio-indicator",
                        options = [{"label" : i, "value" : i} for i in indicators.values()],
                        value = list(indicators.values())[0],
                        input_class_name="me-2",
                        ),
                ],
                width = 4,
            )
        ),
        dbc.row(
            [
                dbc.col(
                    [
                        dbc.label(
                            "Select Years:",
                            className="fw-bold",
                            style={"textDecoration": "underline", "fontSize": 20},),
                        dcc.RangeSlider(
                            id = "years-range",
                            min = 2005,
                            max = 2016,
                            step = 1,
                            values=[2005,2006],
                            marks={
                                2005 : "2005",
                                2005 : "'06",
                                2005 : "'07",
                                2005 : "'08",
                                2005 : "'09",
                                2005 : "'10",
                                2005 : "'11",
                                2005 : "'12",
                                2005 : "'13",
                                2005 : "'14",
                                2005 : "'15",
                                2005 : "2016",
                            },
                            ),
                        dbc.Button(
                            id="my-button",
                            children="Submit",
                            n_clicks=0,
                            color="primary",
                            className="mt-4",
                        )
                    ],
                    width = 6,
                ),
            ]
        ),
        dcc.Store(id = "storage", storage_type="local", data = {}),
        dcc.Interval(id = "time", interval = 1000 * 60, n_intervals = 0),
    ]
)


indicators = {
    "IT.NET.USER.ZS" : "Individuals using the Internet (% of population)",
    "SG.GEN.PARL.ZS" : "Proportion of seats held by women in national parliments (%)",
    "EN.ATM.CO2E.KT" : "CO2 emissions (kt)"
}
