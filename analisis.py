import os
import pandas as pd                         #pip install pandas
from pandas_datareader import data as pdr   #pip install pandas-datareader
import datetime as date
import numpy as np
import matplotlib.pyplot as plt             #pip install matplotlib

"""
Determinar como se comporta en la suba:
    *- La accion
    *- Los indicadores

Para ello se debe hacer:
    *- Establecer cuando esta en suba el activo.
    *- Establecer cuando esta en baja el activo. 
    *- Hacer un analisis de indicadores entre dichas fechas
"""
def max( df ):
    new_df = pd.DataFrame()
    
    max = 0
    min = 999999999

    for i in range(0, len( df )):
        if( max < df['Close'][ i ] ):
            max = df['Close'][ i ]
    print( max )
        #print( str(df['Close'][ i ]) )
    
    

"""
date = [datetime.datetime(2018, 1, 1) + datetime.timedelta(days=x) for x in range(0, 365)]
value = list(np.random.randint(low=0, high=100, size=365))
df['date'] = pd.to_datetime(date)
df.index = df['date']
df['value'] = value
"""

def desviacion( df ):
    print( df.describe() )