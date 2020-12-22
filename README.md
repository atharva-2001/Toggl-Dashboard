# Toggl Dashboard
#### This small project helps you run a Dash app on localhost, in which you can see where you time has been used using data from Toggl track. Its just a more comprehensive report of your data. 
#### You can see the the project on [PYPI](https://pypi.org/project/toggldash/) too. In order to run the program, install the package using the code below:

```
pip install toggldash
```
</br>

#### You can run the dashboard using the python code below:
```python
from toggldash import app
app.run()
```
</br>

#### The program then asks you your toggl credentials. It saves them in a file in your current directory called creds.txt. The file will look something like this
```

    email:yourawesome@email.com
    token:348975634875687ygegy85534653
    workspace_id:5525432
    
```

#### Or you can just create a file with the creds in it. The above creds won't work.
#### By default the app will run on http://127.0.0.1:8050/

</br>

![](https://github.com/bigpappathanos-web/Toggl-Dashboard/blob/main/toggldash/images/Peek%202020-10-12%2013-26.gif?raw=true )

