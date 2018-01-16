import plotly
import plotly.plotly as py
from plotly.graph_objs import *

class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def plot(self, x, y1, y2, y3):

        print("y1: ",y1)
        print("x1: ", x)
        print("y2: ", y3)
        print("x2: ", y3)
        trace0 = Scatter(
            x = x,
            y = y1
        )
        trace1 = Scatter(
            x = x,
            y = y2
        )
        trace2 = Scatter(
            x=x,
            y=y3
        )
        print (trace0)
        print(trace1)
        data = Data([trace0, trace1,trace2])

        py.plot(data, filename='basic-line')

