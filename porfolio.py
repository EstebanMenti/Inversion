import os
import pandas as pd #pip install pandas
from pandas_datareader import data as pdr #pip install pandas-datareader
import datetime as date
import numpy as np
import matplotlib.pyplot as plt  #pip install matplotlib
#--- Para graficos de velas
#from mplfinance import candlestick2_ochl       #pip install mpl_finance
import mplfinance as mpf

from indicadores import *
from graficos import *
from estrategias import *

#import pyfolio                  # pip install pyfolio

def get_Data(index):
    data = pdr.get_data_yahoo(index, start=startdate, end=enddate)
    return(data)


print("Inicio del programa")
simbolos = ['AAPL','MSFT','GLOB','KO','FB','INTC','GE','MELI','GOOG','IBM','XOM']
#simbolos = ['AAPL']
startdate=date.datetime(2010,1,1)
enddate=date.datetime(2020,9,29)

print("Señal de cocodrillo")
for indice in range(0, len(simbolos)):
    ticket = get_Data( simbolos[indice] )
    operacion = cocodrillo( ticket, slow=21, fast=3 )
    print("Ticket: " + simbolos[indice] + "\t Ganacia: " + str(operacion.getGananciaPorcentaje()) )


#aapl.Close.plot()

#obtiene unicamente que se indican
#data_frame = aapl[['Close','MA_50','EMA_50']]
#volumen=aapl[['Volume']]
#print(data_frame)
#print("Volumen")
#print(volumen[0:5])
#grafico_cierre(aapl)
#grafico_vela(aapl)

#data =data_frame[1]

#print("Longitud de la lista: " + str(len(data_frame)))

#print("Elemento de una lista: \n" + str(data_frame[0:1]))
#data_frame.plot(figsize=(16,8))
#print("Precio de Galicia Local")
#print( pdr.get_nasdaq_symbols())





#np.random.seed(19680801)
#data = np.random.lognormal(size=(37, 4), mean=1.5, sigma=1.75)
#labels = list('ABCD')
#fs = 10  # fontsize

#fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(6, 6), sharey=True)
#axs[0, 0].boxplot(data, labels=labels)
#axs[0, 0].set_title('Default', fontsize=fs)

#for ax in axs.flat:
#    ax.set_yscale('log')
#    ax.set_yticklabels([])

#fig.subplots_adjust(hspace=0.4)
#plt.show()

#con la funcion: aapl.loc['2019] filtra, toda la info de ese año