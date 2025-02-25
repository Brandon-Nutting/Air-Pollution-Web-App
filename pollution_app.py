# Importing packages
import pandas as pd
import plotly.express as px # Look into Plotly Graph Objects (More customizable)
from dash import Dash, dcc, html, Input, Output

# Read in the data
pollution_df = pd.read_csv("Input/Air_Quality.csv")

# Use external stylesheet
stylesheet = ['https://codepen.io/chriddyp/pen/bWLegP.css']
app = Dash(__name__, external_stylesheets=stylesheet)

app.layout = html.Div(
    [
        html.Div(
            html.H1(
                "Analysis of air pollution data", style={"textAlign": "center"}
            ),
            className="row",
        ),
        html.Div(dcc.Graph(id="pollution-chart", figure={}), className="row"),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="filter-dropdown",
                        multi=True,
                        options=[
                            {"label": x, "value": x}
                            for x in sorted(pollution_df['Geo Place Name'].unique())
                        ],
                        value=[x for x in pollution_df['Geo Place Name'].unique()],
                    ),
                    className="three columns",
                ),
                html.Div(
                    html.A(
                        id="my-link",
                        children="Click here to view the source data",
                        href="https://www.kaggle.com/datasets/sahirmaharajj/air-pollution-dataset?resource=download",
                        target="_blank",
                    ),
                    className="two columns",
                ),
            ],
            className="row",
        ),
    ]
)

# Callback functions
@app.callback(
    Output(component_id="pollution-chart", component_property="figure"),
    [Input(component_id="filter-dropdown", component_property="value")],
)
def update_graph(selected_value):
    print(f"Currently selected value: {selected_value}")
    
    if len(selected_value) == 0:
        return {}
    else:
        filtered_pollution = pollution_df[pollution_df["Geo Place Name"].isin(selected_value)]
        fig = px.line(
            data_frame=filtered_pollution,
            x = "Start_Date",
            y="Data Value",
            color = "Geo Place Name",
            log_y=True,
            labels={
                "Start Date" : "Reading Date",
                "Data Value" : "Pollution Value",
                "Geo Name Place" : "Location"
            },
        )
        return fig
    
if __name__ == "__main__":
    app.run_server(debug=True)
