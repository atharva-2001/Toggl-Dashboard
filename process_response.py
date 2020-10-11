'''
process response # ! edit
'''

import os
from get_response import get_response

file = open('creds.txt')
lines = file.readlines()

if len(lines) == 0:
    get_response()
else:
    print(lines)
    email = lines[1].split(":")[1][:-1]
    token = lines[2].split(":")[1][:-1]
    workspace_id = lines[3].split(":")[1][:-1]

    print(email, workspace_id, token)