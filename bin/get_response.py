'''
collects creditentials and stores them in a text file
called creds.txt
'''


def fix(lst):
    '''
    just to strip extra spaces
    '''
    res = []
    for item in lst:
        res.append("".join([a for a in list(item) if a != " "]))    
    return res

def get_response():
    email = input("Enter your email address:  ")
    token = input("Enter your secret token:   ")
    workspace_id = input("Enter your workspace id:   ")

    email, token, workspace_id = fix([email, token, workspace_id])
    creds = open("bin/creds.txt", "w")
    creds.write(
    f"""
    email:{email}
    token:{token}
    workspace_id:{workspace_id}
    """)
    
    creds.close()