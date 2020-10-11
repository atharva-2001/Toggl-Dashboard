import pandas as pd 
import plotly
import plotly.graph_objects as go
import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc
import re
from collections import defaultdict, OrderedDict
import requests 
import plotly.graph_objects as go
import numpy as np
import plotly_express as px
import time
from process_response import Response, fetch_creds

email, token, workspace_id = fetch_creds()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    
    html.Div([
        html.P(
            "    Toggl Dashboard",
            style={"font-size": "72px", "fontFamily": "Lucida Console", 'width': '70%', 'display': 'inline-block'},
        ),
        html.Div([
            html.Div(
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=datetime.datetime(2015, 12, 1),
                    max_date_allowed=datetime.datetime(2025, 12, 30),
                    initial_visible_month=datetime.datetime(2017, 8, 5),
                    start_date=datetime.datetime(2020, 8, 10).date(), 
                    end_date= datetime.datetime.now().date() -  datetime.timedelta(days=5), # !fix this
                    display_format='MMM Do, YY',
                    style={"font-size": "20px", "fontFamily": "Lucida Console"})
            ),

            html.Div(
                dcc.Input(
                    id = 'token input',
                    placeholder = 'enter toggl token', 
                    value = token,
                    type = 'password',
                    style={"font-size": "18px", "fontFamily": "Lucida Console"}),
            ),
            
            html.Div(
                dcc.Input(
                    id = 'email input',
                    placeholder = 'enter email address',
                    value = email,
                    style={"font-size": "18px", "fontFamily": "Lucida Console"})
            )],
            style={'width': '30%', 'display': 'inline-block'})
    ]),
     html.Div([
        
        html.Div(dcc.Loading(
            id = 'loading',
            # what's children
            loading_state = {'component_name': 'main sunburst,daily'},
            # fullscreen = True,
            type = 'default'

        )),
        html.Div(    
            dcc.Graph(id = 'main sunburst'), style={'width': '30%', 'display': 'inline-block'}),
        html.Div(
            dcc.Graph(id = 'daily'), style={'width': '60%', 'display': 'inline-block'  })
            ]),
    dcc.Graph(id = 'details-seg'),
    html.Div([
        html.Div(html.H1(children = "daily work done on an average: "), style = {'width': '60%', 'display': 'inline-block' , "fontFamily": "Lucida Console" }),
        html.Div(html.H1(id = 'daily-avg-work'), style ={'width': '40%', 'display': 'inline-block' , "fontFamily": "Lucida Console"}),
        
    ])


    
    # html.Div(id='output-container-date-picker-range')
])

@app.callback(
    dash.dependencies.Output('loading', 'children'),
    [dash.dependencies.Input('loading', 'fullscreen')]
)
def pause(value):
    time.sleep(10)
    return

@app.callback(
    [dash.dependencies.Output('main sunburst', 'figure'),
    dash.dependencies.Output('daily', 'figure'),
    dash.dependencies.Output('details-seg', 'figure'), 
    dash.dependencies.Output('daily-avg-work', 'children'),
    ],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'), 
     dash.dependencies.Input('token input', 'value'),
     dash.dependencies.Input('email input', 'value'),
     ])
def update_output(start_date, end_date, token, mail):
    
    Flag = False

    if start_date is not None:
        start_date = datetime.datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        Flag = True
    if end_date is not None:
        end_date = datetime.datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        Flag = True
    if Flag == False:
        pass # ! raise error
    else:
        pass

    # detailed_df, summary_df = get_response(token, mail, start_date, end_date)
    # sunburst = main_sunburst(summary_df)

    # details_processed = get_processed_df(detailed_df)
    # daily_df, daily = get_daily_work(details_processed)

    # projects_seg  = build_stacked_bar(details_processed)


    res = Response(email=email, 
        token=token, 
        workspace_id=workspace_id, 
        start_date=start_date, 
        end_date=end_date)

    daily_df, daily_bar = res.get_daily_work()

    projects_seg = res.build_stacked_bar()
    sunburst = res.main_sunburst()
    sunburst.show()

    avg_work = str(round(sum(daily_df['work done'].tolist())/len(daily_df), 2)) + 'hrs'
    return (sunburst, daily_bar, projects_seg, avg_work)




if __name__ == '__main__':
    app.run_server(debug=True)