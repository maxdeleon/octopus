import sys
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime as dt
import os
import seaborn as sn
import matplotlib.pyplot as plt

# gets the ticker file and makes it into a list
def getTickerList(tickerFile):
    tickers = []
    with open(tickerFile) as file:
        for line in file:
            tickers.append(line.strip('\n'))
    return tickers

# gets the data using crappy yahoo finance
def getData(watchlist_file):

    end = dt.datetime.today()

    if dt.datetime.now().month != 1:
        start = dt.datetime.now().date().replace(month=1, day=1)
        columns_custom = ['asset','close','previous day','1D change','1D pct change','YTD pct change']
    else:
        start = end - dt.timedelta(days = 252)
        columns_custom = ['asset','close','previous day','1D change','1D pct change','1Y pct change']

    tickers = getTickerList(watchlist_file)    
    
    data = {}
    '''
        C
    ES=F
    ^SPX
    ^NDX
    ^DJI
    ^STOXX
    ^GDAXI
    000001.SS
    ^HSI
    CL=F
    GC=F
    HG=F
    ZS=F
    ^TNX
    EURUSD=X
    GBPUSD=X
    AUDUSD=X
    USDJPY=X
    USDCAD=X
    USDCHF=X
    USDRUB=X
    USDTRY=X
    BTC-USD
    ETH-USD
    LTC-USD
    '''
    rows = []
    for t in tickers:
        data[t] = web.DataReader(t,'yahoo', start, end).reset_index()
        asset_close = data[t].Close.values

        current = round(asset_close[len(asset_close)-1],2)
        one_day = round(asset_close[len(asset_close)-2],2)
        year_ago = asset_close[0]
        day_change = round(current - one_day,3)
        day_change_pct = round(day_change / one_day,3)*100
        year_change_pct = round((current - year_ago)/year_ago,3)*100
        current_row = [t,current,one_day,day_change,day_change_pct,year_change_pct]
        rows.append(current_row)
    
    info_df = pd.DataFrame(data=rows,columns=columns_custom)
    info_df.index = info_df['asset']
    info_df = info_df.drop('asset',axis=1)
    return info_df

# charts the items in a watchlist
def chartWatchlist(watchlist_file,day_range):
    end = dt.datetime.today()
    if day_range == 'YTD':
        if dt.datetime.now().month != 1:
            start = dt.datetime.now().date().replace(month=1, day=1)
        else: pass
    else:
        start = end - dt.timedelta(days = int(day_range))

    tickers = getTickerList('./watchlists/'+watchlist_file) 
    data = pd.DataFrame()
    for t in tickers:
        data[t] = web.DataReader(t,'yahoo', start, end).Close
        #asset_close = data[t].Close.values
    data = ((1 + data.pct_change()).cumprod() - 1)*100

    file_name = 'images/watchlistplot.png'
    delta = end.date() - start.date()
    ax = data.plot()
    ax.set_title('{} watchlist {} Day Cumulative Change'.format(watchlist_file, delta.days))
    ax.set_ylabel('Percent Change (%)')
    plt.tight_layout()
    plt.grid()
    fig = ax.get_figure()
    fig.savefig(file_name)
    return file_name

# creates a correlation table
def correlationTable(watchlist_file,day_range,on_returns=True,visual=True,title='Portfolio',plot_dimensions=(12, 10)):
    end = dt.datetime.today()
    if day_range == 'YTD':
        if dt.datetime.now().month != 1:
            start = dt.datetime.now().date().replace(month=1, day=1)
        else: pass
    else:
        start = end - dt.timedelta(days = int(day_range))
    title = watchlist_file
    tickers = getTickerList('./watchlists/'+watchlist_file) 
    portfolio = pd.DataFrame()
    for t in tickers:
        portfolio[t] = web.DataReader(t,'yahoo', start, end).Close
    
  
    if on_returns:
        portfolio = portfolio.dropna(axis=0)
        portfolio_correlation_matrix = ((1 + portfolio.pct_change()).cumprod() - 1).dropna(axis=0).corr()
    else:
        portfolio_correlation_matrix = portfolio.corr()
    if visual:
        mask = np.zeros_like(portfolio_correlation_matrix)
        mask[np.triu_indices_from(mask)] = True
        with sn.axes_style("dark"):
            f, ax = plt.subplots(figsize=plot_dimensions)
            title += ' Returns Correlation Matrix ' if on_returns else ' Correlation Matrix '
            ax.set_title(title+'('+str(portfolio.index[0])+' - ' +str(portfolio.index[-1])+')')
            ax = sn.heatmap(portfolio_correlation_matrix, annot=True, cmap="icefire",mask=mask, vmax=.3, square=True, linewidths=.5)
        plt.tight_layout()
        plt.savefig('./images/corrmatrix.png')
    else:
        pass
    return './images/corrmatrix.png' 

# creates a watchlist
def createWatchlist(watchlist_name,tickers):
    try:
        tickers = list(tickers.split(','))
    except:
        tickers = []
    watchlist_path = './watchlists/'+watchlist_name
    if not os.path.isfile(watchlist_path):
        with open(watchlist_path, mode='w') as file:
            counter = 0
            for ticker in tickers:
                if ticker != '':
                    file.write(ticker+'\n')
                else: 
                    counter !=1
        return 'Created watchlist under {} and added {} tickers to watchlist'.format(watchlist_name,len(tickers)-counter)
    else:
        return 'Watchlist with name {} already exists!'.format(watchlist_path)

# deletes the watchlist
def deleteWatchlist(watchlist_name):
    watchlist_path = './watchlists/'+watchlist_name
    if os.path.isfile(watchlist_path):
        message = 'rm {}'.format(watchlist_path)
        os.popen(message)
        if not os.path.isfile(watchlist_path):
            return 'Failed to delete {}'.format(watchlist_name)
        else:
            return 'Deleted watchlist under {}'.format(watchlist_name)
            
    else:
        return 'Watchlist with name {} does not exists!'.format(watchlist_name)

def editWatchlist(watchlist_name,action,tickers):
    try:
        tickers = list(tickers.split(','))
    except:
        tickers = []
    
    watchlist_path = './watchlists/'+watchlist_name
    if len(tickers) != 0:
        if os.path.isfile(watchlist_path):
            origional_tickers = getTickerList(watchlist_path)
            if action == 'add':
                with open(watchlist_path,'a') as file:
                    for ticker in tickers:
                        if ticker != '' and ticker not in origional_tickers:
                            file.write(ticker+'\n')
                        else:
                            pass
                return 'Added {} to {}'.format(tickers,watchlist_name)
            elif action == 'remove':
                updated_tickers = []
                for ticker in origional_tickers:
                    if ticker not in tickers and ticker != '':
                        updated_tickers.append(ticker)
                    else:
                        pass
            
                with open(watchlist_path,'w') as file:
                    for ticker in updated_tickers:
                        if ticker != '' and ticker:
                            file.write(ticker+'\n')
                        else:
                            pass
                return 'Removed {} from {}'.format(tickers,watchlist_name)
                
            else:
                return '{} is not a valid command. You can only add or remove tickers'.format(action)
        else:
            return 'Watchlist with name {} does not exists!'.format(watchlist_name)
        
    else:
        return 'No tickers to {} to {}'.format(action,watchlist_name)

def main(argument_list):
    action = argument_list[0]
    
    if action == 'view' and len(argument_list) == 2:
        watchlist_name = argument_list[1]
        watchlist_path = './watchlists/'+watchlist_name
        if os.path.exists(watchlist_path):
            tickers = getTickerList(watchlist_path)
            ticker_string = 'Tickers in {}\n'.format(watchlist_name)
            for ticker in tickers:
                ticker_string += ticker + '\n'
            print('type=TEXT')
            print(ticker_string)
        
        else:
            print('type=TEXT')
            print('Watchlist: {} does not exist!'.format(watchlist_name))
    
    # return a summary of the watchlist
    elif action == 'summary' and len(argument_list) == 2:
        watchlist_name = argument_list[1]
        watchlist_path = './watchlists/'+watchlist_name
        if os.path.exists(watchlist_path):
            df = getData(watchlist_path)
            print('type=TEXT')
            print(df)
        else:
            print('type=TEXT')
            print('Watchlist: {} does not exist!'.format(watchlist_name))
    
    # list the watchlists
    elif action == 'list' and len(argument_list) == 1:
        watch_list_items = os.listdir('./watchlists')
        watchlist_string = 'Saved watchlists:\n'
        counter = 1
        for watchlist in watch_list_items:
            if os.path.isfile('./watchlists/'+watchlist):
                watchlist_string += '({}) {}\n'.format(counter,watchlist)
                counter +=1
            else: pass

        print('type=TEXT')
        print(watchlist_string)
    
    # return a percent chagne chart
    elif action == 'chart' and len(argument_list) == 3:
        print('type=FILE')
        print('{}'.format(chartWatchlist(argument_list[1],argument_list[2])))

    # send a correlation matrix
    elif action == 'cMatrix' and len(argument_list) == 3:
        print('type=FILE')
        print('{}'.format(correlationTable(argument_list[1],argument_list[2])))
    
    # create a watchlist
    elif action == 'create' and len(argument_list) == 3:
        print('type=TEXT')
        print('{}'.format(createWatchlist(argument_list[1],argument_list[2])))

    # delete watchlist
    elif action == 'delete' and len(argument_list) == 2:
        print('type=TEXT')
        print('{}'.format(deleteWatchlist(argument_list[1])))
    
    # add ticker(s) to a watchlist
    elif action == 'add' and len(argument_list) == 3:
        print('type=TEXT')
        print('{}'.format(editWatchlist(argument_list[1],action,argument_list[2])))
    
    # remove ticker(s) from a watchlist
    elif action == 'remove' and len(argument_list) == 3:
        print('type=TEXT')
        print('{}'.format(editWatchlist(argument_list[1],action,argument_list[2])))

    else:
        print('type=TEXT')
        print('Watchlist: Bad number of parameters for function call')


'''


elif action == 'create' and len(argument_list) == 3:
    print('type=TEXT')
    print('{}'.format(createWatchlist(argument_list[1],argument_list[2])))
'''


if __name__ == '__main__':
    parameters = sys.argv
    parameters.pop(0)
    main(parameters)