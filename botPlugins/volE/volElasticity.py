import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import sys
import pandas_datareader.data as web

def main(args):
    parameters = args
    parameters.pop(0)
    ticker = parameters[0]
    if 'dateRange=' in parameters[1]:
        dates=parameters[1].strip('dateRange=').split('|')
        dates[0] = dt.date(dates[0])
        dates[1] = dt.date(dates[1])
        image_file = plot_vol(ticker,volatility_elasticity(ticker,dates,custom_range=True))
    else:
        image_file = plot_vol(ticker,volatility_elasticity(ticker,int(parameters[1]),custom_range=False))

    print('type=FILE')
    print(image_file)

def plot_vol(ticker, df):
        plt.style.use('seaborn-whitegrid')
        fig = plt.figure(figsize=(15,7.5))
        gs = fig.add_gridspec(2, hspace=0,wspace=0)
        (ax1, ax2)= gs.subplots(sharex='col')
        ax1.plot(df.Date, df.Real_Vol, label=ticker+' Realized Volatility', color='red')
        ax2.bar(df.Date, df.Vol_Elasticity, label=ticker+' Volatilisitic Elasticity of Returns', color='blue')
        ax1.set_ylabel('Volatility ($\sigma$)',size=12)
        ax2.set_ylabel('Volatility Elasticity (dP/d$\sigma$)',size=12)
        fig.suptitle(ticker+' Volatility Breakdown',size=15)
        file_name = 'images/volBreakdown.png'
        ax1.grid()
        ax2.grid()
        plt.legend()
        plt.tight_layout()
        plt.savefig(file_name)
        return file_name

def volatility_elasticity(ticker=str, lookback_days='dateRange', custom_range=bool):
        
    def import_data(ticker=str, lookback_days=int):
        if not custom_range:
            end = dt.datetime.today()
            start = end - dt.timedelta(days = lookback_days)
        else:
            start = lookback_days[0]
            end = lookback_days[1]
        
        ticker = ticker.upper()
        #df = yf.download(ticker, start, end, progress=False)
        df = web.DataReader(ticker,'yahoo', start, end)
        df = df.dropna()
        df['Date'] = df.index
        df.index = range(0, len(list(df.index)))
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
        
        def returns(df):
            df['Simple_Return'] = df['Close'].pct_change()
            df['Abs_Return'] = [price-df['Close'][n-1] if n>=1 else 0 for n,price in enumerate(df.Close)]
            df['Log_Return'] = np.log(df['Adj Close']/df['Close'].shift(1))
            return df
  
        return returns(df)

    def add_volatility(df, period=str):   
        if period <= 30:
            window = 5
        elif period > 30 and period <= 90:
            window = 10
        else:
            window = 20
                
        df['Real_Vol'] = df['Log_Return'].rolling(window=window).std(ddof=0)*np.sqrt(252)
        
        ve = df.Simple_Return/df.Real_Vol.pct_change()
        for n,vol in enumerate(ve):
            if vol > 5:
                ve[n] = 5
            elif vol < -5:
                ve[n] = -5
                
        df['Vol_Elasticity'] = ve
        df['Vol_Elasticity_Dummy'] = [1 if abs(vol_e)>1 else 0 for vol_e in df.Vol_Elasticity]
        
        return df

    return add_volatility(import_data(ticker, lookback_days),lookback_days)

if __name__ == '__main__':
    main(sys.argv)