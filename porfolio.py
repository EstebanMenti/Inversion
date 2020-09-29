import pandas as pd #pip install pandas
from pandas_datareader import data as pdr #pip install pandas-datareader
import datetime as date
import numpy as np
import matplotlib.pyplot as plt  #pip install matplotlib
#import pyfolio                  # pip install pyfolio

def get_Data(index):
    data = pdr.get_data_yahoo(index, start=startdate, end=enddate)
    return(data)

startdate=date.datetime(2020,1,1)
enddate=date.datetime(2020,9,29)

aapl=get_Data('aapl')

#aapl.head()
#aapl.Close.plot()

print(aapl)


np.random.seed(19680801)
data = np.random.lognormal(size=(37, 4), mean=1.5, sigma=1.75)
labels = list('ABCD')
fs = 10  # fontsize

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(6, 6), sharey=True)
axs[0, 0].boxplot(data, labels=labels)
axs[0, 0].set_title('Default', fontsize=fs)

for ax in axs.flat:
    ax.set_yscale('log')
    ax.set_yticklabels([])

fig.subplots_adjust(hspace=0.4)
plt.show()