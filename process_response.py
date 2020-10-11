'''
process response # ! edit
'''

import os
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
from get_response import get_response

file = open('creds.txt')
lines = file.readlines()

if len(lines) == 0:
    get_response()
else:
    email = lines[1].split(":")[1][:-1]
    token = lines[2].split(":")[1][:-1]
    workspace_id = lines[3].split(":")[1][:-1]

class response():
    def __init__(self, email, token, workspace_id,  start_date, end_date):
        self.email = email
        self.token = token
        self.workspace_id = workspace_id
        self.sd = start_date
        self.ed = end_date
    

    def get_response(self):
        '''
        returns dataframes back
        in a list [detailed, summary]
        '''
        URL = 'https://api.track.toggl.com/reports/api/v2/details?workspace_id={}&since={}&until={}&user_agent={}'.format(
            str(self.workspace_id), str(self.sd), str(self.ed), self.email
        )
        username = token # also the token
        password = 'api_token'
        cols = ['description', 'start', 'end', 'updated', 'dur', 'project', 'project_hex_color']
        df_raw = defaultdict(list)
        ind, data, data_in = 1, [], [0]

        while len(data_in) != 0:
            
            URL = URL + '&page=' + str(ind)
            response = requests.get(URL, auth = (username, password)).json()

            data_in = response['data']
            data += data_in
            for col in cols:
                for item in data_in:
                    df_raw[col].append(item[col]) # * fix this linting error
            ind += 1

        detailed_df = pd.DataFrame.from_dict(df_raw)

        URL = 'https://api.track.toggl.com/reports/api/v2/summary?workspace_id=4482767&since={}&until={}&user_agent={}'.format(
            str(self.sd), str(self.ed), self.email
        )
        response = requests.get(URL, auth = (username, password)).json()

        df = defaultdict(list)
        data = response['data']
        for project in data:
            tasks = project['items'] 
            for task in tasks:
                df['task'].append(task['title']['time_entry'])
                df['task time duration'].append(task['time'])
                df['project'].append(project['title']['project'])
                df['project time duration'].append(project['time'])
                df['project color'].append(project['title']['hex_color'])
        df = pd.DataFrame.from_dict(df)
        summary_df = df.dropna()

        self.summary_df = summary_df
        self.detailed_df = detailed_df

        return [detailed_df, summary_df]

    def get_processed_df(self, df):
        '''
        process the detailed df
        '''
        df = self.detailed_df
        df['start'] = df['start'].apply(lambda x: datetime.datetime.strptime(x.split("+")[0], '%Y-%m-%dT%H:%M:%S'))
        df['end'] = df['end'].apply(lambda x: datetime.datetime.strptime(x.split("+")[0], '%Y-%m-%dT%H:%M:%S'))
        df['updated'] = df['updated'].apply(lambda x: datetime.datetime.strptime(x.split("+")[0], '%Y-%m-%dT%H:%M:%S'))
        df['start_day'] = df['start'].apply(lambda x: x.date())
        df['end_day'] = df['end'].apply(lambda x: x.date())

        df_daily_raw = defaultdict(list)
        rows = []

        for index, row in df.iterrows():
            # if end and start day is equal
            if row['start_day'] != row['end_day']:
                row1, row2 = row.to_dict(), row.to_dict()
                start = row['start']
                end = row['end']

                end_day = row['end_day']

                mid =  (datetime.datetime.combine(row['end_day'], datetime.datetime.min.time()))

                dur1 = (mid - start).seconds * 1000
                dur2 = (end - mid).seconds * 1000
                # print(dur1, dur2)
                
                row1['dur'] = dur1
                row2['dur'] = dur2

                row1['end'] = pd.Timestamp((datetime.datetime.combine(row['start_day'], datetime.datetime.max.time())))
                row2['start'] = pd.Timestamp(mid)

                # row1['start_day'] = row['start_day']
                row1['end_day'] = row1['end'].date()
                row2['start_day'] = mid.date()
                rows.append([index, row1, row2])
        # print(df.columns)
        for item in rows:
            tmp = pd.DataFrame(np.insert(df.values, item[0],values = list(item[1].values()), axis = 0 ))
            tmp = pd.DataFrame(np.insert(tmp.values, item[0]+1,values = list(item[2].values()), axis = 0 ))
            tmp.drop(item[0] + 2, inplace = True)
        tmp.columns = df.columns
        return df 