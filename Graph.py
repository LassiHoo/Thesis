import plotly
from plotly import tools
import plotly.graph_objs as go
from plotly.graph_objs import *
import plotly.plotly as py
import numpy as np


class graph:
    def __init__(self):
        plotly.tools.set_credentials_file(username='LassiPee', api_key='qNE4nDymb62oYrcqhegQ')

    def ccdf(self, datain, datain2, name1, name2):
        #
        # cumsum = np.cumsum(datain)
        #
        # trace = Scatter(x=[i for i in range(len(cumsum))], y= 10.0 * cumsum / np.linalg.norm(cumsum),
        #                 marker=dict(color='rgb(150, 25, 120)'))
        # layout = go.Layout(
        #     title="Cumulative Distribution Function"
        # )
        #
        # fig = go.Figure(data=go.Data([trace]), layout=layout)
        # py.plot(fig, filename='cdf-dataset')
        #
        # # retrieve event times and latencies from the file
        # compute the CDF
        cdfx = np.sort(datain)
        cdfy = np.linspace(1 / len(datain), 1.0, len(datain))
        # plot the CDF
        trace1 = Scatter(
            x=cdfx,
            y=cdfy,
        )
        cdfx2 = np.sort(datain)
        cdfy2 = np.linspace(1 / len(datain), 1.0, len(datain))
        # plot the CDF
        trace2 = Scatter(
            x=cdfx2,
            y=cdfy2,
        )

        fig = tools.make_subplots(rows=2, cols=1)

        fig.append_trace(trace2, 1, 1)
        fig.append_trace(trace1, 2, 1)
        fig['layout'].update(height=600, width=600, title='Stacked subplots')
        py.plot(fig, filename='stacked-subplots')
        py.plot(trace1, filename='ccdf')

    def plot(self, x, y1, y2, y3, y4, y5, y1_name, y2_name, y3_name, y4_name, y5_name):

        trace1 = Scatter(
            x= x,
            y= y1,
            name=y1_name,
        )
        trace2 = Scatter(
            x=x,
            y=y2,
            name = y2_name,
        )
        trace3 = Scatter(
            x=x,
            y=y3,
            name = y3_name,
        )
        trace4 = Scatter(
            x=x,
            y=y4,
            name = y4_name,
        )
        trace5 = Scatter(
            x=x,
            y=y5,
            name=y5_name,
        )
        fig = tools.make_subplots(rows=5, cols=1)

        fig.append_trace(trace3, 1, 1)
        fig.append_trace(trace2, 2, 1)
        fig.append_trace(trace1, 3, 1)
        fig.append_trace(trace4, 4, 1)
        fig.append_trace(trace5, 5, 1)
        fig['layout'].update(height=600, width=600, title='Stacked subplots')
        py.plot(fig, filename='stacked-subplots')
