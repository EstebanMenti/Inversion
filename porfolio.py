import os
import pandas as pd                         #pip install pandas
from pandas_datareader import data as pdr   #pip install pandas-datareader
import datetime as date
import numpy as np
import matplotlib.pyplot as plt  #pip install matplotlib
#--- Para graficos de velas
#from mplfinance import candlestick2_ochl       #pip install mpl_finance
#import mplfinance as mpf


from download import *
from indicadores import *
from graficos import *
from estrategias import *
from correlacion import *
from operacion import *
from analisis import *

print("***********************************************************************")
print("***********************************************************************")
print("***********************************************************************")
formato = "%d-%m-%Y %H:%M:%S"

print("\n\nInicio del programa: ", date.date.today().strftime(formato)+"\n")

tickers = ['AGRO.BA','ALUA.BA','AUSO.BA','BHIP.BA','BMA.BA','BOLT.BA','BPAT.BA','BRIO.BA',
           'BYMA.BA','CADO.BA','CAPX.BA','CECO2.BA','CELU.BA','CEPU.BA','CGPA2.BA','COME.BA',
           'CRES.BA','CTIO.BA','CVH.BA','DGCU2.BA','EDN.BA','ESME.BA','FERR.BA','GAMI.BA','GARO.BA',
           'GCLA.BA','GGAL.BA','GRIM.BA','HARG.BA','HAVA.BA','INAG.BA','INTR.BA','INVJ.BA','IRCP.BA',
           'IRSA.BA','LOMA.BA','LEDE.BA','LONG.BA','METR.BA','MIRG.BA','MOLA.BA','MOLI.BA','MORI.BA',
           'OEST.BA','PAMP.BA','PATA.BA','PGR.BA','ROSE.BA','SAMI.BA','SEMI.BA','SUPV.BA',
           'TECO2.BA','TGNO4.BA','TGSU2.BA','TRAN.BA','TXAR.BA','YPFD.BA']

tickersUSA = ['AAPL']#,'GGAL.BA','GGAL','MSFT','GLOB','KO','FB','INTC','GE','MELI','GOOG','IBM','XOM'] 
simbolos = tickersUSA 

print("\n\n***********************************************************************")
print("DOWNLOAD DATA")
años = 1
startdate = date.date.today() - date.timedelta(365*años)
enddate   = date.date.today()
print("Periodo. Desde: " + str(startdate) + " Hasta: " + str(enddate) )
diccinario = download(tickets = simbolos, años = años, enddate=enddate)

print("\n\n***********************************************************************")
print('ESTRATEGIAS')
ticket = diccinario.keys()

mc = 0
mbah = 0
mrsi = 0
mrsima = 0

for i in diccinario:

    a = pd.DataFrame( diccinario[ i ]['Close'] )
    e_c = cocodrilo( i, a )
    e_bah = buy_and_hold(i, diccinario[ i ])
    e_rsi = rsi_sobrecompra_sobreventa( i, diccinario[ i ] )
    e_r_m = estrategia_rsi_media(i, diccinario[ i ])
        

    mc += e_c.get_ganancia_porcentual()
    mbah += e_bah.get_ganancia_porcentual()
    mrsi += e_rsi.get_ganancia_porcentual()
    mrsima += e_r_m.get_ganancia_porcentual()

    print(i + "\tCocodrilo: " + str(e_c.get_ganancia_porcentual()) + "% (" + str(e_c.get_day_in()) + ")" +
    "\tComprar y Retener: " + str(e_bah.get_ganancia_porcentual()) + "% (" + str(e_bah.get_day_in()) + ")" +
    "\tRSI: " + str(e_rsi.get_ganancia_porcentual()) + "% (" + str(e_rsi.get_day_in()) + ")" +
    "\tRSI Cocodrilo: " + str(round(e_r_m.get_ganancia_porcentual(),1)) + "% (" + str(e_r_m.get_day_in()) + ")")
print("--------------------------------------------------------------------------------------------")

mc = mc / len(diccinario)
mbah /= len(diccinario)
mrsi /= len(diccinario)
mrsima /= len(diccinario)
print( "MEDIA")
print("\tCocodrilo: " + str(round(mc,2))+ "%" + 
"\tComprar y Retener: " + str(round(mbah,2)) +"%" +  
"\tRSI: " + str(round(mrsi,2)) + "%"
"\tRSI Cocodrilo: " + str(round(mrsima,2)) +"%")
print("***********************************************************************")

print("\n\n***********************************************************************")
print("CORRELACION ENTRE ACTIVOS")
print( correlacion( diccinario ) )
print("***********************************************************************")

print("\n\n***********************************************************************")
print("ANALISIS DE DATOS")
desviacion( diccinario['AAPL'] )
print("***********************************************************************")


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
