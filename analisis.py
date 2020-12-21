import os
import pandas as pd                         #pip install pandas
from pandas_datareader import data as pdr   #pip install pandas-datareader
import datetime as date
import numpy as np
import matplotlib.pyplot as plt  #pip install matplotlib
# Desviación típica 
#np.std(datos, 0)

def desviacion(df):
    print( df.describe() )