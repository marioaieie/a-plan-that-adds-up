# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read data
sources = pd.read_csv('sources.csv')
sources.sort_values('source', inplace=True)

sources['area'] = 42
sources['power'] = sources['power_density'] * sources['area'] / 1000. * 24
# sources['power'] = 20
# sources['area'] = sources['power'] / sources['power_density'] * 1000 / 24.

sources['cumulative_power'] = sources['power'].cumsum()

knobs = []
inputs = []
states = []
for source in sources['source']:
    knobs += [daq.Knob(
        id=source.lower(),
        min=0,
        max=50,
        value=2,
        label=source,
        size=64,
        style={'display': 'inline-block'},
    ),
    ]
    inputs += [Input(source.lower(), 'value')]
    states += [State(source.lower(), 'label')]


app.layout = html.Div(children=[
    html.H1(children='A plan that adds up'),

    html.Div(children=[
        html.Div(id='knobs',
                 children=knobs,
                 style={'display': 'inline-block',
                        'width': '600px'},
                 ),
        dcc.Graph(
            id='production-stack',
            style={'display': 'inline-block',
                   'width': '400px',},
            config={'displayModeBar': False, }
        ),
        daq.Tank(
            id='tank',
            max=50,
            showCurrentValue=True,
            units='kWh/d',
            style={'margin-left': '50px',
                   'display': 'inline-block'},
            label='Total',
            labelPosition='bottom',
        ),
    ]),
])


@app.callback(Output('production-stack', 'figure'),
              inputs,
              states)
def update_plot(*params):
    for label, value in zip(params[len(params)//2:],
                            params[:len(params)//2]):
        sources.loc[sources['source'] == label, 'power'] = value

    data = []
    for idx, source in sources.iterrows():
        data += [{'x': [0],
                  'y': [source['power']],
                  'text': source['source'],
                  'textposition': 'auto',
                  'showlegend': False,
                  'opacity': 0.6,
                  'hoverinfo': 'text',
                  'type': 'bar'}]
    figure = {
        'data': data,
        'layout': {
            'title': 'Production Stack',
            'barmode': 'stack',
        }
    }
    return figure

@app.callback(Output('tank', 'value'),
              [Input('production-stack', 'figure')])
def fill_tank(figure):
    return sources['power'].sum()


if __name__ == '__main__':
    app.run_server(debug=True)
