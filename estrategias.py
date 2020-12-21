import os
import math
import datetime
from indicadores import *
from operacion import *
import pandas as pd  

class cocodrilo( operatiOnOnActve ):
    def __init__(self, ticket, df, slow=21, fast=3, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df
        self.__slow = slow
        self.__fast = fast
        self.__tipo = tipo
        super().__init__( ticket = self.__ticket, tipo = self.__tipo )
        self.ejecutar()
        

    def ejecutar(self):

        ms = ma(self.__df, self.__slow, add=False) 
        mf = ma(self.__df, self.__fast, add=False)

        cruceUp=False
        
        for indice in range(self.__slow, len(mf)):
            if( mf.values[indice] > ms.values[indice] ):
                if( cruceUp == False):
                    cruceUp = True 
                    super().load_operacion(self.__df.values[indice,0], self.__df.index[indice].to_pydatetime(),1, 'compra')

                    #operacion.load_operacion(date = mf.index[indice].to_pydatetime(), typeOperacion= True, valorTicket = mf.values[indice] )

            if( mf.values[indice] < ms.values[indice] ):
                if( cruceUp == True ):
                    cruceUp = False
                    super().load_operacion(self.__df.values[indice,0], self.__df.index[indice].to_pydatetime(),1, 'venta')
                    #operacion.load_operacion(date = mf.index[indice].to_pydatetime(), typeOperacion= False, valorTicket = mf.values[indice] )

        if(super().get_cantidad_activos() != 0 ):
            super().load_operacion(self.__df.values[-1,0], self.__df.index[-1].to_pydatetime(), 1, 'venta')


class buy_and_hold( operatiOnOnActve ):
    #Comprar y retener
    def __init__(self, ticket, df, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df['Close']
        self.__tipo = tipo
        super().__init__( ticket = self.__ticket, tipo = self.__tipo )
        self.ejecutar()

    def ejecutar(self):
        super().load_operacion(self.__df[ 0 ], self.__df.index[ 0 ].to_pydatetime(), 1, 'compra')
        super().load_operacion(self.__df[-1 ], self.__df.index[-1 ].to_pydatetime(), 1, 'venta' )

        
class rsi_sobrecompra_sobreventa( operatiOnOnActve ):
    #Utiliza limite de sobre compra y sobre venta para ejecutar la accion
    def __init__(self, ticket, df, rsi = 14, sobrecompra=(70/100), sobreventa=(30/100), tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df
        self.__rsi = rsi
        self.__sobrecompra = sobrecompra
        self.__sobreventa = sobreventa
        self.__tipo = tipo
        super().__init__( ticket = self.__ticket, tipo = self.__tipo )
        self.ejecutar()
    
    def ejecutar(self):
        _rsi = rsi(self.__df, self.__rsi, add=False)

        comprado=False
        #print(self.__df[20:21])
        for p in range(self.__rsi, len(_rsi)):

            if( (_rsi[ p ] > self.__sobrecompra) and (comprado == False) ):
                comprado = True
                super().load_operacion(self.__df['Close'].values[ p ], self.__df.index[ p ].to_pydatetime(),1, 'compra')
            if( (_rsi[ p ] < self.__sobreventa) and (comprado == True) ):
                comprado = False
                super().load_operacion(self.__df['Close'].values[ p ], self.__df.index[ p ].to_pydatetime(),1, 'venta')
    
        if(super().get_cantidad_activos() != 0 ):
            super().load_operacion(self.__df['Close'].values[ p ], self.__df.index[ -1 ].to_pydatetime(),1, 'venta')
        

class estrategia_rsi_media( operatiOnOnActve ):
    def __init__(self, ticket, df, rsi = 14, tipo ='accionbyma'):
        
        self.__df = df
        self.__rsi = rsi
        self.__tipo = tipo
        super().__init__(ticket = ticket, tipo = self.__tipo)
        self.ejecutar()

    def ejecutar(self):
        _rsi = pd.DataFrame(rsi(self.__df, self.__rsi, add=False) ) 

        slow = 21 
        fast = 3
        ms = ma(_rsi[self.__rsi:], slow, add=False) 
        mf = ma(_rsi[self.__rsi:], fast, add=False)

        cruceUp=False
        
        for indice in range(slow, len(mf)):
            i = indice + self.__rsi
            
            if( mf.values[indice] > ms.values[indice] ):
                if( _rsi.values[i] < 0.8 ):   
                    if( cruceUp == False):
                        cruceUp = True
                        super().load_operacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'compra') 
                                            
            if( mf.values[indice] < ms.values[indice] ):
                if( _rsi.values[i] > 0.2 ):  
                    if( cruceUp == True ):
                        cruceUp = False
                        super().load_operacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'venta')
                
        if(super().get_cantidad_activos() != 0 ):
            super().load_operacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'venta')

class estrategia_rsi_desviacion( operatiOnOnActve ):
    def __init__(self, ticket, df, rsi = 20, sobrecompra=(70/100), sobreventa=(30/100), tipo ='accionbyma'):
        self.__df = df
        self.__rsi = rsi
        super().__init__(ticket = ticket, tipo = tipo)
        self.ejecutar()
    
    def ejecutar(self):
        _rsi = pd.DataFrame(rsi(self.__df, self.__rsi, add=False) )
        df = pd.DataFrame( _rsi.describe() )
        min = df.values[3,0]
        media = df.values[5,0]
        max = df.values[6,0]
        