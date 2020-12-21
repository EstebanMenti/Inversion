import os
import pandas as pd #pip install pandas
import yfinance as yf
import datetime as date

#Baja todos los datos de los tickets y lo retorna en un diccionario.
def download(tickets, enddate = date.date.today(), años=10, intervalo ='1d' ):
    #Establece el periodo de datos a bajar
    startdate = date.date.today() - date.timedelta(365*años)
    enddate   = date.date.today()

    #Baja los datos y los ordena en un diccionario
    diccionario={}
    for indice in range(0, len(tickets)):
        df = yf.download(tickets[indice], start=startdate, end=enddate , interval = intervalo)
        diccionario[ tickets[indice] ] = df.dropna() 
    
    #print(diccionario)
    return(diccionario)


 # fetch data by interval (including intraday if period < 60 days)
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# (optional, default is '1d')