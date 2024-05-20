# dash-bootstrap-components : Makes it easier to manage layout of application. 
# Pandas Datareader : Retrieves data via an API. 
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from pandas_datareader import wb

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

countries = wb.get_countries()
countries["capitalCity"].replace({"" : None}, inplace = True)
countries.dropna(subset = ["capitalCity"], inplace = True)
countries = countries[["name", "iso3c"]]
countries = countries[countries["name"] != "Kosovo"]
countries.rename(columns = {"name":"country"}, inplace = True)

indicators = {
    "IT.NET.USER.ZS" : "Individuals using the Internet (% of population)",
    "SG.GEN.PARL.ZS" : "Proportion of seats held by women in national parliments (%)",
    "EN.ATM.CO2E.KT" : "CO2 emissions (kt)"
}

def update_wb_data():
    """ Retreives updaetd data from API connection. """
    df = wb.download(
        indicator = (list(indicators)), country = countries['iso3c'],
        start = 2005, end = 2016
    )
    df = df.reset_index()
    df.year = df.year.astype(int)
    
    # Add country ISO3 to main df
    df = pd.merge(df, countries, on="country")
    df = df.rename(columns=indicators)
    return df

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        "Comparison of World Bank Country Data",
                        style={"textAlign": "center"},),
                    dcc.Graph(id="my_choropleth", figure={})
                ],
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Label("Select Data Set:",
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label(
                            "Select Years:",
                            className="fw-bold",
                            style={"textDecoration": "underline", "fontSize": 20},),
                        dcc.RangeSlider(
                            id = "years-range",
                            min = 2005,
                            max = 2016,
                            step = 1,
                            value=[2005,2006],
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
                            id="my_button",
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
        dcc.Interval(id = "timer", interval = 1000 * 60, n_intervals = 0),
    ]
)

@app.callback(Output("storage","data"), Input("timer","n_intervals"))
def store_data(n_time):
    dataframe = update_wb_data()
    return dataframe.to_dict("records")

@app.callback(
    Output("my_choropleth", "figure"),
    Input("my_button", "n_clicks"),
    Input("storage", "data"),
    State("years-range","value"),
    State("radio-indicator", "value"),
)
def update_graph(n_clicks, stored_dataframe, years_chosen, indct_chosen):
    dff = pd.DataFrame.from_records(stored_dataframe)
    print(years_chosen)
    
    if years_chosen[0] != years_chosen[1]:
        dff = dff[dff.year.between(years_chosen[0], years_chosen[1])]
        dff = dff.groupby(["iso3c", "country"])[indct_chosen].mean()
        dff = dff.reset_index()
        
        fig = px.choropleth(
            data_frame=dff, 
            locations = "iso3c",
            color=indct_chosen,
            scope="world",
            hover_data={"iso3c" : False, "country" : True},
            labels = {
                indicators["SG.GEN.PARL.ZS"] : "% parliment women",
                indicators["IT.NET.USER.ZS"] : "pop % using interet",
            },
        )
        fig.update_layout(
            geo = {"projection" : {"type" : "natural earth"}},
            margin = dict(l=50, r = 50, t = 50, b = 50),
        )
        return fig
    
    if years_chosen[0] == years_chosen[1]:
        dff = dff[dff["year"].isin(years_chosen)]
        fig = px.choropleth(
            data_frame=dff, 
            locations = "iso3c",
            color=indct_chosen,
            scope="world",
            hover_data={"iso3c" : False, "country" : True},
            labels = {
                indicators["SG.GEN.PARL.ZS"] : "% parliment women",
                indicators["IT.NET.USER.ZS"] : "pop % using interet",
            },
        )
        fig.update_layout(
            geo = {"projection" : {"type" : "natural earth"}},
            margin = dict(l=50, r = 50, t = 50, b = 50),
        )
        return fig
    
if __name__ == "__main__":
    app.run_server(debug = True)