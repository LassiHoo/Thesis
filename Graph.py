import plotly
import plotly.plotly as py
from plotly.graph_objs import *

class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def plot(self, x, y1, y2, y3, y1_name, y2_name, y3_name):

        print("x: ",x)
        print("y1: ", y1)
        print("y2: ", y2)
        print("y3: ", y3)
        trace0 = Scatter(
            x = x,
            y = y1,
            name = y1_name
        )
        trace1 = Scatter(
            x = x,
            y = y2,
            name = y2_name
        )
        trace2 = Scatter(
            x=x,
            y=y3,
            name = y3_name
        )
        print (trace0)
        print(trace1)
        data = Data([trace0, trace1,trace2])

        py.plot(data, filename='basic-line')

