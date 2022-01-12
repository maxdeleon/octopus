import numpy as np
import pandas as pd
import math
import json
import os.path
from os import path

# indicators from A old repository of mine so definitely check the numbers
def ewma(close, period):
  ewma = close.ewm(span=period, min_periods=0, adjust=True, ignore_na=True).mean() #Weighted moving average 50
  return ewma

def rsi(data, period):
    diff = data.diff(1).dropna()        # diff in one field(one day)
    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=period-1 so we get decay alpha=1/period
    up_chg_avg   = up_chg.ewm(com=period-1 , min_periods=period).mean()
    down_chg_avg = down_chg.ewm(com=period-1 , min_periods=period).mean()
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def bollinger(data, period, band_width = 2):
    ma = data.window(period).mean()
    std = data.window(period).std()
    upper = ma + band_width*ma
    lower = ma - band_width*ma
    return ma,upper,lower


INDICATORS = {'ewma':ewma,
            'rsi':rsi,
            'bollinger':bollinger}