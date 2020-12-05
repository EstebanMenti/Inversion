import os
import pandas as pd                         #pip install pandas
import datetime as date


#determina la correlacion entre los tickets pasados (Ej: AGRO.BA','ALUA.BA')
def correlacion( diccionario ):
    
    #Ordena los datos (obtiene en base cierre)
    df = pd.DataFrame()
    for i in diccionario:
        df[ i ] = diccionario[i]['Close']

    #determina la correlacion entre activos
    corr = round(df.corr(),3)   #redondeo de decimales
    return( corr )



