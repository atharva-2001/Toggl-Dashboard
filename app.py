import pandas as pd 
import plotly
import plotly.graph_objects as go
import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc
import re
from collections import defaultdict
import requests 
import plotly.graph_objects as go

API_token = '7f45ea45a1833ac7e127047a738e4264' # * get from the dashboard 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def get_response(token, email, start_date, end_date):
    '''
    returns dataframes back
    in a list [detailed, summary]
    '''
    URL = 'https://api.track.toggl.com/reports/api/v2/details?workspace_id=4482767&since={}&until={}&user_agent={}'.format(
        str(start_date), str(end_date), email
    )
    username = token # also the token
    # print(token)
    password = 'api_token'
    
    cols = ['description', 'start', 'end', 'updated', 'dur', 'project', 'project_hex_color']

    df_raw = defaultdict(list)
    ind = 1
    data = []
    data_in = [0]
    while len(data_in) != 0:
        URL = URL + '&page=' + str(ind)
        response = requests.get(URL, auth = (username, password)).json()
        # print(response)
        data_in = response['data']
        data += data_in
        for col in cols:
            for item in data_in:
                df_raw[col].append(item[col])
        ind += 1
    detailed_df = pd.DataFrame.from_dict(df_raw)

    URL = 'https://api.track.toggl.com/reports/api/v2/summary?workspace_id=4482767&since={}&until={}&user_agent={}'.format(
        str(start_date), str(end_date), email
    )
    response = requests.get(URL, auth = (username, password)).json()

    df = defaultdict(list)
    data = response['data'] # is a list
    for project in data:
        tasks = project['items'] # is a list too, containing dictionaries 
        for task in tasks:
            df['task'].append(task['title']['time_entry'])
            df['task time duration'].append(task['time'])
            df['project'].append(project['title']['project'])
            # df['project name'].append(project['title']['project'])
            df['project time duration'].append(project['time'])
            df['project color'].append(project['title']['hex_color'])
    df = pd.DataFrame.from_dict(df)
    summary_df = df.dropna()


    return [detailed_df, summary_df]


def build_sunburst_data(df, parents, labels,values, string = 'total'):
    
    main_parents = list(set(parents))
    main_values = []
    
    for main_parent in  main_parents:
        tmp = []
        for parent, label, value in zip(parents, labels, values):
            if parent == main_parent:
                tmp.append(value)
        main_values.append(sum(tmp))
    
    parents += [string] * len(main_parents)
    labels += main_parents
    values += main_values

    parents.append("")
    labels.append(string)
    values.append(0.5*sum(values))

    return parents, labels, values


def main_sunburst(df):
    parents, labels, values = build_sunburst_data(df, df['project'].tolist(), df['task'].tolist(),df['task time duration'].tolist(), string = 'total')
    fig = go.Figure()
    fig.add_trace(
        go.Sunburst(
            values = values,
            parents = parents,
            labels = labels,
            branchvalues = 'total', 
            # maxdepth = 2,
            textinfo = "none"
        )
    )
    return fig





app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.P(
            "Toggl Dashboard",
            style={"font-size": "72px", "fontFamily": "Lucida Console"},
        ),
    html.Div([
        html.Div([
            html.Div(
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=datetime.datetime(2015, 12, 1),
                    max_date_allowed=datetime.datetime(2025, 12, 30),
                    initial_visible_month=datetime.datetime(2017, 8, 5),
                    end_date=datetime.datetime(2020, 9, 30).date(), 
                    start_date= datetime.datetime(2020, 8, 30).date())
            # , style={'width': '40%', 'display': 'inline-block'}
            ),

            html.Div(
                dcc.Input(
                    id = 'token input',
                    placeholder = 'enter toggl token', 
                    value = API_token,
                    type = 'password')
            # ), style={'width': '30%', 'display': 'inline-block'}
            ),
            
            html.Div(
                dcc.Input(
                    id = 'email input',
                    placeholder = 'enter email address',
                    value = 'aryaatharva18@gmail.com')
                # ), style={'width': '30%', 'display': 'inline-block'}
            )],
            style={'width': '30%', 'display': 'inline-block'}), 

        dcc.Graph(id = 'main sunburst', style={'width': '70%', 'display': 'inline-block'})
    ])
    # html.Div(id='output-container-date-picker-range')
])


@app.callback(
    dash.dependencies.Output('main sunburst', 'figure'),
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

    detailed_df, summary_df = get_response(token, mail, start_date, end_date)
    fig = main_sunburst(summary_df)

    return (fig)

    




    
    

    





if __name__ == '__main__':
    app.run_server(debug=True)