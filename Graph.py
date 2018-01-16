import plotly
import plotly.plotly as py
from plotly.graph_objs import *

class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def plot(self, x1 ,y1, x2, y2):

        print("y1: ",y1)
        print("x1: ", x1)
        print("y2: ", y2)
        print("x2: ", x2)
        trace0 = Scatter(
            x1,
            y1
        )
        trace1 = Scatter(
            x2,
            y2
        )
        print (trace0)
        print(trace1)
        data = Data([trace0, trace1])

        py.plot(data, filename='basic-line')

