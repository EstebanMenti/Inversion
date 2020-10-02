import os
import pandas as pd #pip install pandas
from pandas_datareader import data as pdr #pip install pandas-datareader
import datetime as date
import numpy as np
import matplotlib.pyplot as plt  #pip install matplotlib
#import pyfolio                  # pip install pyfolio

def get_Data(index):
    data = pdr.get_data_yahoo(index, start=startdate, end=enddate)
    return(data)


def ma(df, n):
    ma=pd.Series(pd.Series.rolling(df['Close'],n).mean(), name='MA_' + str(n))
    df = df.join(ma)
    return df

def ema(df, n):
    ema = pd.Series(pd.Series.ewm(df['Close'], span = n, min_periods = n -1, adjust = False).mean(), name='EMA_' + str(n))
    df = df.join(ema)
    return df


print("Inicio del programa")
startdate=date.datetime(2001,1,1)
enddate=date.datetime(2020,9,29)

aapl=get_Data('aapl')

#agrega la media movil de 50
aapl = ma(aapl, 50)

#agrega la media movil ponderada de 50
aapl = ema(aapl,50)

#ma_50 = ma(aapl, 50) 
#ma_50.head()

aapl.head()
#aapl.Close.plot()

data_frame = aapl[['Close','MA_50','EMA_50']]

fig = plt.figure(figsize=(16,8))
plt.subplot(2,1,1)
plt.plot( aapl[['Close']] )
#plt.axhline(y=0, color='r')
plt.title("Precio de cierre")


plt.subplot(2,1,2)
plt.plot( aapl[['MA_50']] )
plt.title("MA_50")

plt.show()

#data_frame.plot(figsize=(16,8))
#print("Precio de Galicia Local")
#print( pdr.get_nasdaq_symbols())





#np.random.seed(19680801)
#data = np.random.lognormal(size=(37, 4), mean=1.5, sigma=1.75)
labels = list('ABCD')
fs = 10  # fontsize

#fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(6, 6), sharey=True)
#axs[0, 0].boxplot(data, labels=labels)
#axs[0, 0].set_title('Default', fontsize=fs)

#for ax in axs.flat:
#    ax.set_yscale('log')
#    ax.set_yticklabels([])

#fig.subplots_adjust(hspace=0.4)
#plt.show()