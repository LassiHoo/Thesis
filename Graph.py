import plotly
from plotly import tools
import plotly.graph_objs as go
from plotly.graph_objs import *
import plotly.plotly as py
import numpy as np


class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def plot(self, x, y1, y2, y3, y4, y5, y1_name, y2_name, y3_name, y4_name, y5_name):

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
        cumsum = np.cumsum(y2)

        trace = Scatter(x=[i for i in range(len(cumsum))], y=10 * cumsum / np.linalg.norm(cumsum),
                           marker=dict(color='rgb(150, 25, 120)'))
        layout = go.Layout(
            title="Cumulative Distribution Function"
        )

        fig = go.Figure(data=go.Data([trace]), layout=layout)
        py.plot(fig, filename='cdf-dataset')

        # trace1 = Scatter(
        #     x= x,
        #     y= y1,
        #     name=y1_name,
        # )
        # trace2 = Scatter(
        #     x=x,
        #     y=y2,
        #     name = y2_name,
        # )
        # trace3 = Scatter(
        #     x=x,
        #     y=y3,
        #     name = y3_name,
        # )
        # trace4 = Scatter(
        #     x=x,
        #     y=y4,
        #     name = y4_name,
        # )
        # trace5 = Scatter(
        #     x=x,
        #     y=y5,
        #     name=y5_name,
        # )
        # fig = tools.make_subplots(rows=5, cols=1)
        #
        # fig.append_trace(trace3, 1, 1)
        # fig.append_trace(trace2, 2, 1)
        # fig.append_trace(trace1, 3, 1)
        # fig.append_trace(trace4, 4, 1)
        # fig.append_trace(trace5, 5, 1)
        # fig.append_trace(trace6, 6, 1)
        # fig['layout'].update(height=600, width=600, title='Stacked subplots')
        # py.plot(fig, filename='stacked-subplots')
