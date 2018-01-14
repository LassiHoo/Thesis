import plotly
import plotly.plotly as py
from plotly.graph_objs import *

class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def plot(self):

        trace0 = Scatter(
            x=[1, 2, 3, 4],
            y=[10, 15, 13, 17]
        )
        trace1 = Scatter(
            x=[1, 2, 3, 4],
            y=[16, 5, 11, 9]
        )
        data = Data([trace0, trace1])

        py.plot(data, filename='basic-line')

