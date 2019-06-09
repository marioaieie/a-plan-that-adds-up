# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import pandas as pd

# external_stylesheets = ['style.css']

# app = dash.Dash()
# # Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
# application = app.server

server = flask.Flask(__name__)
application = dash.Dash(__name__, server=server)


# Read data
sources = pd.read_csv('sources.csv')
sources.sort_values('source', inplace=True)

sources['area'] = 42
sources['power'] = sources['power_density'] * sources['area'] / 1000. * 24
# sources['power'] = 20
# sources['area'] = sources['power'] / sources['power_density'] * 1000 / 24.

# sources['cumulative_power'] = sources['power'].cumsum()

knobs = []
inputs = []
states = []
for source in sources['source']:
    knobs += [daq.Knob(
        id=source.lower(),
        min=0,
        max=500 if source != 'Plants' else 1000,
        value=10,
        label=source,
        size=64,
        style={'display': 'inline-block'},
    ),
    ]
    inputs += [Input(source.lower(), 'value')]
    states += [State(source.lower(), 'label')]

app.layout = html.Div(children=[
    html.H1(children='A plan that adds up', style={'text-align': 'center', }),

    html.Div(children=[
        html.Div(id='knobs',
                 children=[html.H2(children='Area covered per person (m^2/p) ',
                                   style={'text-align': 'center'}), ] + knobs,
                 style={'display': 'inline-block',
                        'width': '450px'},
                 ),
        html.Div(id='production-div',
                 children=[html.H2(children='Daily energy production per person (kW/h/d)',
                                   style={'text-align': 'center'}),
                           dcc.Graph(
                               id='production-stack',
                               style={'display': 'inline-block',
                                      'width': '400px',
                                      'height': '480px'},
                               config={'displayModeBar': False, }
                           ), ],
                 style={'display': 'inline-block',
                        'width': '450px'},
                 ),
        html.Div(id='area-div',
                 children=[html.H2(children='Fraction of Great Britain covered for energy production',
                                   style={'text-align': 'center'}),
                           dcc.Graph(
                               id='area-stack',
                               style={'display': 'inline-block',
                                      'width': '400px',
                                      'height': '480px'},
                               config={'displayModeBar': False, }
                           ), ],
                 style={'display': 'inline-block',
                        'width': '450px'},
                 ),
    ]),
])


@app.callback(Output('production-stack', 'figure'),
              inputs,
              states)
def update_plot(*params):
    for label, value in zip(params[len(params) // 2:],
                            params[:len(params) // 2]):
        sources.loc[sources['source'] == label, 'area'] = value

    sources['power'] = sources['power_density'] * sources['area'] / 1000. * 24

    data = []
    for idx, source in sources.iterrows():
        data += [{'x': [0],
                  'y': [source['power']],
                  'text': source['source'],
                  'textposition': 'auto',
                  'showlegend': False,
                  'opacity': 0.6,
                  'hoverinfo': 'y',
                  'type': 'bar'}]
    data += [{'x': [5],
              'y': [50 - sources['power'].sum().round(2)],
              'text': 'Missing',
              'textposition': 'auto',
              'showlegend': False,
              'opacity': 0.6,
              'hoverinfo': 'y',
              'type': 'bar'}]
    figure = {
        'data': data,
        'layout': {
            'barmode': 'stack',
            'yaxis': {'range': [0, 59]},
            'xaxis': {
                'showgrid': False,
                'ticks': '',
                'showticklabels': False,
            }
        }
    }
    return figure


@app.callback(Output('area-stack', 'figure'),
              [Input('production-stack', 'figure')])
def update_area_plot(*params):
    # for label, value in zip(params[len(params) // 2:],
    #                         params[:len(params) // 2]):
    #     sources.loc[sources['source'] == label, 'area'] = value
    #
    # sources['power'] = sources['power_density'] * sources['area'] / 1000. * 24

    population = 60  # millions
    total_area = 209331  # km^2
    data = []
    # for idx, source in sources.iterrows():
    #     data += [{'x': [0],
    #               'y': [source['area'] * population / total_area],
    #               'text': source['source'],
    #               'textposition': 'auto',
    #               'showlegend': False,
    #               'opacity': 0.6,
    #               'hoverinfo': 'y',
    #               'type': 'bar'}]
    data += [{'x': [0],
              'y': [(sources['area'] * population / total_area).sum() * 100],
              'text': '',
              'textposition': 'auto',
              'showlegend': False,
              'opacity': 0.6,
              'hoverinfo': 'y',
              'type': 'bar'}]
    figure = {
        'data': data,
        'layout': {
            'barmode': 'stack',
            'yaxis': {'range': [0, 100]},
            'xaxis': {
                'showgrid': False,
                'ticks': '',
                'showticklabels': False,
            }
        }
    }
    return figure


if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run_server(debug=True, port=8080)