import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly import graph_objs as go
from data import Data
import flask

server = flask.Flask(__name__)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    '//fonts.googleapis.com/css?family=Bitter'
]

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])
server = app.server


navbar = html.Nav(
    children=[
        html.Div('Melius'),
        html.Img(id='logo', src=app.get_asset_url("TFD_Logo.png"))
    ]
)

dates = ['1', '2', '3', '4', '5']
trace1_m = go.Bar(
    x=dates, y=[20, 21, 23, 3, 3],
    name='Steigend',
marker={'color': 'green'}
)
trace2_m = go.Bar(
    x=dates, y=[12, 18, 29, 34, 14],
    name='Stagnierend',
marker={'color': 'yellow'}
)
trace3_m = go.Bar(
    x=dates, y=[20, 5, 12, 12, 16],
    name='Fallend',
    marker={'color': 'red'}
)

data_m = [trace3_m, trace2_m, trace1_m]
layout = go.Layout(
    barmode='stack',
    xaxis=dict(tickvals=dates),
    title="Fachentwicklung Mathematik"
)
fig_m = go.Figure(data=data_m, layout=layout)

trace1_s = go.Bar(
    x=dates, y=[10, 12, 9, 8, 12],
    name='Steigend',
marker={'color': 'green'}
)
trace2_s = go.Bar(
    x=dates, y=[10, 12, 18, 19, 20],
    name='Stagnierend',
marker={'color': 'yellow'}
)
trace3_s = go.Bar(
    x=dates, y=[1, 3, 2, 1, 2],
    name='Fallend',
    marker={'color': 'red'}
)

data_s = [trace3_s, trace2_s, trace1_s]
layout = go.Layout(
    barmode='stack',
    xaxis=dict(tickvals=dates),
    title="Entwicklung Social Skills"
)
fig_s = go.Figure(data=data_s, layout=layout)



container = html.Div(id="grid_container", children=[
    html.Div(children=[
        html.H2('Regionen'),
        dcc.Dropdown(
            id="my-dropdown",
            options=[
                {'label': u'Süd', 'value': 'Süd'},
                {'label': u'West', 'value': 'West'},
                {'label': 'Nord', 'value': 'Nord'},
                {'label': 'BBB', 'value': 'BBB'}
            ],
            value=['Süd', 'West', 'Nord', 'BBB'],
            multi=True
        )
    ], id="filter_section", className="pane"),
    html.Div(children=[
    ], id="fellows_stats", className="pane"),
    html.Div(children=[
    ], id="fellows_total", className="pane"),
    html.Div(children=[
    ], id="fellows_region", className="pane"),
    html.Div(id="bar_math", className="pane", children=[
        dcc.Graph(figure=fig_m, style={'width': '100%', 'height': '100%'})
    ]),
    html.Div(id="bar_social", className="pane", children=[
        dcc.Graph(figure=fig_s, style={'width': '100%', 'height': '100%'})
    ])


])


app.layout = html.Div(children=[
    navbar,
    container
])

region_f = {"West": 92,
            "Süd":64,
            "Nord": 45,
            "BBB": 55}

@app.callback(
    dash.dependencies.Output('fellows_region', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_pie(value):
    values = []
    labels = []
    for reg in value:
        values.append(region_f[reg])
        labels.append(reg)
    piedata = dcc.Graph(style={'width': '100%', 'height': '100%'}, id="pie", figure=go.Figure(data=[go.Pie(values=values, labels=labels)], layout=go.Layout(title="Fellows pro Region")))
    return  piedata
    

@app.callback(
    dash.dependencies.Output('fellows_stats', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_fellow_stats(value):
    graph = dcc.Graph(style={'width': '100%', 'height': '100%'},
              id='fellow_count',
              figure={
                  'data': [
                      {'x': [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
                       'y': [getFellowSum(2009, value), getFellowSum(2010, value), getFellowSum(2011, value),
                             getFellowSum(2012, value), getFellowSum(2013, value), getFellowSum(2014, value),
                             getFellowSum(2015, value), getFellowSum(2016, value), getFellowSum(2017, value),
                             getFellowSum(2018, value), getFellowSum(2019, value), getFellowSum(2020, value),
                             getFellowSum(2021, value)], 'type': 'trend', 'name': 'Anzahl an Fellows'}
                  ],
                  'layout': {
                      'title': 'Verlauf Anzahl an Fellows'
                  }
              }
              )
    return graph

@app.callback(
    dash.dependencies.Output('fellows_total', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_fellow_stats(value):
    sum = 0
    sum = getFellowSum(2021, value)
    content = html.Div(children=[
        html.Div(str(sum), className="total_pane_value"),
        html.Div('Fellows', className="total_pane_name")
    ])

    return content

def getFellowSum(year, regions):
    sum = 0
    data = fellows["years"][str(year)]
    for region in regions:
        sum += data[region.lower()]
    return sum


fellows = {
  "years": {
    "2009": {
      "nord": 20,
      "bbb": 10,
      "süd": 15,
      "west": 21
    },
        "2010": {
      "nord": 18,
      "bbb": 30,
      "süd": 23,
      "west": 37
    },
        "2011": {
      "nord": 12,
      "bbb": 23,
      "süd": 32,
      "west": 18
    },
        "2012": {
      "nord": 20,
      "bbb": 35,
      "süd": 23,
      "west": 41
    },
        "2013": {
      "nord": 20,
      "bbb": 34,
      "süd": 43,
      "west": 35
    },
        "2014": {
      "nord": 20,
      "bbb": 45,
      "süd": 23,
      "west": 51
    },
        "2015": {
      "nord": 20,
      "bbb": 23,
      "süd": 41,
      "west": 58
    },
        "2016": {
      "nord": 34,
      "bbb": 42,
      "süd": 29,
      "west": 47
    },
        "2017": {
      "nord": 20,
      "bbb": 49,
      "süd": 31,
      "west": 48
    },
        "2018": {
      "nord": 10,
      "bbb": 20,
      "süd": 30,
      "west": 40
    },
        "2019": {
      "nord": 35,
      "bbb": 45,
      "süd": 54,
      "west": 82
    },
    "2020": {
          "nord": 37,
          "bbb": 46,
          "süd": 57,
          "west": 89
      },
      "2021": {
          "nord": 45,
          "bbb": 55,
          "süd": 64,
          "west": 92
      }
  }
}

if __name__ == '__main__':
    df = Data()
    app.run_server(debug=False)
