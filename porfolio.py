import pandas as pd #pip install pandas
from pandas_datareader import data as pdr #pip install pandas-datareader
import datetime as date
#import matplotlib.pylot as plt
#import pyfolio

def get_Data(index):
    data = pdr.get_data_yahoo(index, start=startdate, end=enddate)
    return(data)

startdate=date.datetime(2020,1,1)
enddate=date.datetime(2020,9,28)

aapl=get_Data('aapl')
print(aapl)