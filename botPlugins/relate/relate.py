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



def analyzeReturns(ticker2,ticker1,lookback_days,custom_range):
    if not custom_range:
        end = dt.datetime.today()
        start = end - dt.timedelta(days = lookback_days)
    else:
        start = lookback_days[0]
        end = lookback_days[1]

    df1= web.DataReader(ticker1,'yahoo', start, end)
    df2= web.DataReader(ticker2,'yahoo', start, end)

    returns1 = df1.Close.pct_change().dropna(axis=0)
    returns2 = df2.Close.pct_change().dropna(axis=0)

    b, m = leastSquaresFit(returns2.to_numpy(),returns1.to_numpy())

    x_fit = np.linspace(returns2.min(),returns2.max(),int(10*len(returns1)))
    y = [m*x + b for x in x_fit]
    
    plt.scatter(returns2,returns1,c='r',label='Returns')
    plt.ylabel('{} Returns'.format(ticker1))
    plt.xlabel('{} Returns'.format(ticker2))
    plt.plot(x_fit,y,c='b',label='Least Squares Fit')
    plt.title('{} vs {} Returns Scatter Plot ({} Days)'.format(ticker2,ticker1,lookback_days))
    plt.grid()
    plt.tight_layout()
    plt.legend()
    file_name = 'images/returnScatter.png'
    plt.savefig(file_name)
    return file_name

def leastSquaresFit(x,f):
    n = len(x) - 1
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    for i in range(0,n+1):
        c1 += x[i]
        c2 += x[i]*x[i]
        c3 += f[i]
        c4 += f[i]*x[i]

    g = c1*c1-c2*(n+1)
    a0 = (c1*c4-c2*c3)/g
    a1 = (c1*c3-c4*(n+1))/g

    return a0, a1

if __name__ == '__main__':
    parameters = sys.argv
    parameters.pop(0)
    ticker1 = parameters[0]
    ticker2 = parameters[1]
    if len(parameters) > 3:
        if 'dateRange' in parameters[2]:
            dates=parameters[1].split('|')
            image_file = analyzeReturns(ticker1,ticker2,dates,custom_range=True)
        else:
            image_file = analyzeReturns(ticker1,ticker2,int(parameters[2]),custom_range=False)
    else:
            image_file = analyzeReturns(ticker1,ticker2,100,custom_range=False)

    print('type=FILE')
    print(image_file)