import os
import matplotlib.pyplot as plt
import pandas as pd
import quandl as ql
from APIKEY import *

ql.ApiConfig.api_key = KEY


'''def pullData():
    yield_ = ql.get("USTREASURY/YIELD")
    today = yield_.iloc[-1,:]
    month_ago = yield_.iloc[-30,:]
    df = pd.concat([today, month_ago], axis=1)
    df.columns = ['today', 'month_ago']


    fig = plt.figure(figsize=(20,7))

    ax1 = fig.add_subplot(121)
    df.plot(style={'today': 'ro-', 'month_ago': 'bx--'}
            ,title='Treasury Yield Curve, %',ax=ax1);

    ax2 = fig.add_subplot(122)
    font_size=14
    bbox=[0, 0, 1, 1]
    ax2.axis('off')
    mpl_table = ax2.table(cellText = df.values, rowLabels = df.index, bbox=bbox, colLabels=df.columns)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    ax1.grid()
    plt.tight_layout()
    plt.savefig('./images/yieldCurve.png')
    
    print('type=FILE')
    print('./images/yieldCurve.png')
    '''

def pullData():
    yield_ = ql.get("USTREASURY/YIELD")
    today = yield_.iloc[-1,:]
    yesterday = yield_.iloc[-2,:]
    month_ago = yield_.iloc[-30,:]
    df = pd.concat([today,yesterday, month_ago], axis=1)
    df.columns = ['current: {}'.format( pd.to_datetime(yield_.index[-1]).date()),'previous day', 'month_ago']
    return df, yield_

def plotData(df):
    fig = plt.figure(figsize=(20,7))

    ax1 = fig.add_subplot(121)
    df.plot(style={df.columns[0]: 'ro-','previous day':'go--', 'month_ago': 'bx--'}
            ,title='Treasury Yield Curve, %',ax=ax1);
    
    ax2 = fig.add_subplot(122)
    font_size=14
    bbox=[0, 0, 1, 1]
    ax2.axis('off')
    mpl_table = ax2.table(cellText = df.values, rowLabels = df.index, bbox=bbox, colLabels=df.columns)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    ax1.grid()
    plt.tight_layout()
    plt.savefig('./images/yieldCurve.png')
    print('type=FILE')
    print('./images/yieldCurve.png')

if __name__ == '__main__':
    df, yield_ = pullData()
    plotData(df)