import os
import pandas as pd #pip install pandas
import yfinance as yf
import datetime as date

#Baja todos los datos de los tickets y lo retorna en un diccionario.
def download(tickets, enddate = date.date.today(), años=10 ):
    #Establece el periodo de datos a bajar
    startdate = date.date.today() - date.timedelta(365*años)
    enddate   = date.date.today()

    #Baja los datos y los ordena en un diccionario
    diccionario={}
    for indice in range(0, len(tickets)):
        df = yf.download(tickets[indice], start=startdate, end=enddate , interval='1d')
        diccionario[ tickets[indice] ] = df 
    
    #print(diccionario)
    return(diccionario)
