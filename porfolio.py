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

qqq = ["AAPL", "MSFT", "AMZN", "TSLA", "FB", "GOOGL", "GOOG", "NVDA", "PYPL", "ADBE"]
tickersUSA = ['AAPL','TSLA','BABA','GGAL.BA','GGAL','MSFT','GLOB','KO','FB','INTC','GE','MELI','GOOG','IBM','XOM', 'SPY'] 



simbolos = qqq 

print("\n\n***********************************************************************")
print("DOWNLOAD DATA")
años = 5
startdate = date.date.today() - date.timedelta(365*años)
enddate   = date.date.today()
print("Periodo. Desde: " + str(startdate) + " Hasta: " + str(enddate) )
diccinario = download(tickets = simbolos, años = años, enddate=enddate, intervalo='1d')
print("***********************************************************************")

print("\n\n***********************************************************************")
print('ANALISIS DE DATOS')
max( diccinario['AAPL'] )

print("***********************************************************************")

print("\n\n***********************************************************************")
print('CALCULO DE ESTRATEGIAS')

#Conforma una lista de lista.  Cada sub-lista contiene las clases de estrategias sobre un activo.
lista_estrategia_activo=[]
for i in diccinario:

    lista_estrategia = []

    df = pd.DataFrame( diccinario[ i ]['Close'] )
    
    lista_estrategia.append( cocodrilo( i, df ) )
    lista_estrategia.append( buy_and_hold(i, diccinario[ i ]) )
    lista_estrategia.append( rsi_sobrecompra_sobreventa( i, diccinario[ i ] ) )
    lista_estrategia.append( estrategia_rsi_media(i, diccinario[ i ]) )

    _rsi = pd.DataFrame(rsi(diccinario[ i ], 20, add=False))
    df = pd.DataFrame( _rsi.describe() )
    min = df.values[3,0]
    max = df.values[6,0]

    lista_estrategia.append( rsi_sobrecompra_sobreventa( i, diccinario[ i ], sobrecompra= max, sobreventa=min ) )

    lista_estrategia_activo.append( lista_estrategia )

print("\n\n***********************************************************************")
print('SELECCION DE ESTRATEGIAS DE MAYOR RENDIMIENTO')
#Busca las acciones que estan dando mayor ganancia
df = pd.DataFrame( columns=['RSI'] )
for i in range(0, len(lista_estrategia_activo)):
    estrategia = lista_estrategia_activo[i][3]
    df = df.append({'RSI' : estrategia.get_ganacia_porcentual_diario()} , ignore_index=True)

minimo = df.quantile(50/100).values[0]

#Eliminar de la lista de estrategias, todas aquellas que tengan un rendimiento menor al 50%
lista_estrategia_activo = [x for x in lista_estrategia_activo if (x[3].get_ganacia_porcentual_diario() > minimo) ]

print("\n\n***********************************************************************")
print('IMPRIME LAS ESTRATEGIAS\n')

for i in range(0, len(lista_estrategia_activo)):
    ticket =  lista_estrategia_activo[i][3].get_ticket()
    print(ticket + '\t', end="")
    for x in range( 0, len(lista_estrategia_activo[ i ] )):
        ganancia = lista_estrategia_activo[ i ][ x ].get_ganancia_porcentual()
        dias =  lista_estrategia_activo[ i ][ x ].get_day_in()
        print(str(ganancia) + ' (' + str(dias) +  ')\t', end='' )

    print("")    
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
