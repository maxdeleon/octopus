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
from indicators import *

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

def pullData(ticker,days,custom_range=False):
    if not custom_range:
        end = dt.datetime.today()
        start = end - dt.timedelta(days = days)
    else:
        start = days[0]
        end = days[1]
    df = web.DataReader(ticker,'yahoo', start, end)

    return df

def computeIndicator(data,indicator, indicator_range):
    output = indicator(data,indicator_range)
    return output

def plot(data,indicator):
    axs = plt.subplots(2,figsize=(15,7))
    x = data.index
    axs[0].plot(x,data['Close'])
    axs[1].plot(x,data)


if __name__ == '__main__':
    parameters = sys.argv
    parameters.pop(0)
    ticker = parameters[0]
    indicator = parameters[2]
    indicator_range = parameters[3]

    if indicator in INDICATORS.keys():
        if 'dateRange' in parameters[1]:
            dates=parameters[1].split('|')
            df = pullData(ticker,dates,custom_range=True)
            df[indicator] = computeIndicator(df['Close'],
                                                INDICATORS[indicator],
                                                indicator_range)

        else:
            df = pullData(ticker,int(parameters[1]),custom_range=False)
            df[indicator] = computeIndicator(df['Close'],
                                                INDICATORS[indicator],
                                                indicator_range)
            x = df.index
            y = df[indicator]


        #print('type=FILE')
        #print(image_file)
    else:
        print('type=TEXT')
        print('Indicator not found!')