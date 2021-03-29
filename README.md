


![](https://github.com/atharva-2001/Toggl-Dashboard/blob/main/toggldash/images/Untitled.png?raw=true)

<p align = "center">
<a href=""><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/atharva-2001/Toggl-Dashboard?style=for-the-badge"></a> <a href=""><img alt="GitHub License" src="https://img.shields.io/github/license/atharva-2001/Toggl-Dashboard?style=for-the-badge"></a> <a href=""><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/atharva-2001/Toggl-Dashboard?style=for-the-badge"></a> <a href=""><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/atharva-2001/Toggl-Dashboard?style=for-the-badge"></a> <a href=""><img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/atharva-2001/Toggl-Dashboard?style=for-the-badge"></a>
</p>
This small project helps you run a Dash app on localhost, in which you can see where your time has been used using data from Toggl track. It's just a more comprehensive report of your data. 
You can see the the project on <a href = https://pypi.org/project/toggldash/>PyPI</a> too. In order to run the program, install the package using the code below:

```
pip install toggldash
```
</br>

You can run the dashboard using the python code below:
```python
from toggldash import app
app.run()
```
</br>

The program then asks you your toggl credentials. It saves them in a file in your current directory called creds.txt. The file will look something like this
```

    email:yourawesome@email.com
    token:348975634875687ygegy85534653
    workspace_id:5525432
    
```
Or you can just create a file with the creds in it. The above creds won't work.
By default the app will run on http://127.0.0.1:8050/

</br>

![](https://github.com/bigpappathanos-web/Toggl-Dashboard/blob/main/toggldash/images/Peek%202020-10-12%2013-26.gif?raw=true )

