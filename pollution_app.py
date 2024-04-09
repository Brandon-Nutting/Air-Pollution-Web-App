# Importing packages
import pandas as pd
import plotly.express as px # Look into Plotly Graph Objects (More customizable)
from dash import Dash, dcc, html, Input, Output

# Read in the data
pollution_df = pd.read_csv("Input/Air_Quality.csv")

# Use external stylesheet
stylesheet = ['https://codepen.io/chriddyp/pen/bWLegP.css']
app = Dash(_name_, external_stylesheets=stylesheet)

# Determines the layout of the app
# Displays three dropdowns as one row
app.layout = html.Div([
   html.Div(
       html.H1("Analysis of air pollution",
               style={"textAlign":"center"}),
       className="row"),
   html.Div(
       dcc.Graph(id = 'Pollution Chart', figure=fig),
       className="row"),
   html.Div(
       dcc.Dropdown(
           id='Filter Dropdown',
           multi=True,
           options=[
               {"label" : x, "value": x}
               for x in sorted(pollution_df['Geo Place Name'].unique())],
        ),
       className="three columns",
   ),
   html.Div(
       html.A(
           id="Data Link",
           children="Click on link to view source data",
           href="https://www.kaggle.com/datasets/sahirmaharajj/air-pollution-dataset?resource=download",
           target="_blank",
           style = {"color" : "blue", "fontSize" : "40px"}
       ),
       className="two columns",
   ),
], className="row", # className accepts classes from stylesheets.
), 
