import pandas as pd
import plotly.graph_objects as go

tmp = pd.read_csv('/home/atharva/workspace/intense toggl viz/bin/tmper.csv')

labels = tmp['labels'].tolist()
parents= tmp['parents'].tolist()
values = tmp['values'].tolist()

labels = [label if label not in set(parents) else label + '(label)' for label in labels]
print(labels)
fig = go.Figure(go.Sunburst(
    labels = labels,
    parents= parents,
    values = values
))
fig.show()


fig =go.Figure(go.Sunburst(
    labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
))
# Update layout for tight margin
# See https://plotly.com/python/creating-and-updating-figures/
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

fig.show()