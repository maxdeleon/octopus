import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import pandas_datareader.data as web
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import sys

def plot(ticker,days,custom_range=False,volume=True):
    if not custom_range:
        end = dt.datetime.today()
        start = end - dt.timedelta(days = days)
    else:
        start = days[0]
        end = days[1]

    df = web.DataReader(ticker,'yahoo', start, end)


        # Create subplots and mention plot grid size
    rows = 2 if volume else 1
    row_width = [0.2, 0.7] if volume else [0.7]
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=row_width)

    # Plot OHLC on 1st row
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                    low=df["Low"], close=df["Close"], name="OHLC"), 
                    row=1, col=1
    )

    # Bar trace for volumes on 2nd row without legend
    if volume:
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], showlegend=False), row=2, col=1)

    fig.update_layout(template='plotly_white')
    # Do not show OHLC's rangeslider plot 
    fig.update(layout_xaxis_rangeslider_visible=False)

    
    fig.update_layout(title='{} {} Day Price Graph'.format(ticker,days),yaxis_title='{} Price'.format(ticker))
    file_name = 'images/candleplot.png'

    fig.write_image(file_name)
    return file_name

if __name__ == '__main__':
    parameters = sys.argv
    parameters.pop(0)
    ticker = parameters[0]
    volume = parameters[2]
    if 'dateRange' in parameters[1]:
        dates=parameters[1].split('|')
        image_file = plot(ticker,dates,custom_range=True,volume=volume)
    else:
        image_file = plot(ticker,int(parameters[1]),custom_range=False,volume=volume)

    print('type=FILE')
    print(image_file)