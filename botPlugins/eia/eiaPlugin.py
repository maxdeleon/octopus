import os
import sys
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from eiaLogin import *
EIA_PATH = './dataSources/'

# gets the ticker file and makes it into a list
def getSourceDict(file_name):
    source_dict = {}
    with open(file_name) as file:
        for line in file:
            if line != '':
                line = line.split(':')
                source_dict[line[0]] = line[1].strip('\n')
            else:
                pass
    return source_dict

def get_series(name,code,api_key=EIA_PRIVATE_KEY):
    URL = 'http://api.eia.gov/series/?api_key='+api_key+'&series_id='+code
    r = requests.get(url = URL)
    data = np.array((r.json())['series'][0]['data'])
    df = pd.DataFrame(data=data,columns=['date',name])
    df = df.iloc[::-1]
    df.index = df.date
    df = df.drop('date',axis=1)
    df.index = pd.to_datetime(df.index.astype(str), format='%Y%m')
    return df.astype(float)

# very quick method for pulling EIA data through the bot
def main(arg):
    action = arg[0]

    try: 
        if action == 'csv':
            sources = getSourceDict(EIA_PATH+arg[1])
            df = get_series(arg[2],sources[arg[2]])
            df.index = pd.to_datetime(df.index)
            # basic greater than parameter
            if len(arg) == 4:
                df = df.loc[df.index.year >= int(arg[3])]
            else: pass
            # save to csv
            df.to_csv('./temp/data.csv')

            print('type=FILE')
            print('./temp/data.csv')

        elif action == 'chart':
            sources = getSourceDict(EIA_PATH+arg[1])
            df = get_series(arg[2],sources[arg[2]])
            # basic greater than parameter
            df.index = pd.to_datetime(df.index)
            if len(arg) == 4:
                df = df.loc[df.index.year >= int(arg[3])]
            else: pass
            # make quick plot
            plt.subplots(figsize=(15,7))
            plt.plot(df.index,df[arg[2]],label=arg[2],c='b')
            plt.grid()
            plt.tight_layout()
            plt.legend()
            # save to file
            plt.savefig('./images/eia_plot.png')

            print('type=FILE')
            print('./images/eia_plot.png')
        # lists the sources
        elif action == 'sources':
            sources = getSourceDict(EIA_PATH+arg[1])
            return_string = ''
            for key in sources.keys():
                return_string += '{} -> {}\n'.format(key,sources[key])
            print('type=TEXT')
            print(return_string)

        # pull a raw series from the EIA
        elif action == 'raw':
            df = get_series(arg[1],arg[1])
            df.index = pd.to_datetime(df.index)

            # save to csv
            df.to_csv('./temp/data.csv')

            print('type=FILE')
            print('./temp/data.csv')
        else:
            print('type=TEXT')
            print('Unknown parameter.')
    
    except:
        print('type=TEXT')
        print('Plugin error')


if __name__ == '__main__':
    parameters = sys.argv[1:]
    main(parameters)
