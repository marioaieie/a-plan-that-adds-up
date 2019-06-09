import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import flask



# app = dash.Dash()
# # Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
# application = app.server

server = flask.Flask(__name__)
application = dash.Dash(__name__, server=server)


application.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        This is Dash running on Elastic Beanstalk.
    '''),

    daq.Knob(
        id='my-daq-knob',
        value=8,
        min=0,
        max=10
    ),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run_server(debug=True, port=8080, )
