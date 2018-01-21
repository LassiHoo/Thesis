import plotly
from plotly import tools
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go

class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def plot(self, x, y1, y2, y3, y4, y1_name, y2_name, y3_name, y4_name):

        # print("x: ",x)
        # print("y1: ", y1)
        # print("y2: ", y2)
        # print("y3: ", y3)
        # trace0 = Scatter(
        #     x = x,
        #     y = y1,
        #     name = y1_name
        # )
        # trace1 = Scatter(
        #     x = x,
        #     y = y2,
        #     name = y2_name
        # )
        # trace2 = Scatter(
        #     x=x,
        #     y=y3,
        #     name = y3_name
        # )
        # print (trace0)
        # print(trace1)
        # data = Data([trace0, trace1,trace2])
        #
        # py.plot(data, filename='basic-line')
        trace1 = go.Scatter(
            x= x,
            y= y1,
            name=y1_name,
        )
        trace2 = go.Scatter(
            x=x,
            y=y2,
            name = y2_name,
        )
        trace3 = go.Scatter(
            x=x,
            y=y3,
            name = y3_name,
        )
        trace4 = go.Scatter(
            x=x,
            y=y4,
            name = y4_name,
        )
        fig = tools.make_subplots(rows=4, cols=1)

        fig.append_trace(trace3, 1, 1)
        fig.append_trace(trace2, 2, 1)
        fig.append_trace(trace1, 3, 1)
        fig.append_trace(trace4, 4, 1)
        fig['layout'].update(height=600, width=600, title='Stacked subplots')
        py.plot(fig, filename='stacked-subplots')
