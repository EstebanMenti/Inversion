import os
import math
import datetime
from indicadores import *
from operacion import *
import pandas as pd  

class Cocodrilo():
    def __init__(self, ticket, df, slow=21, fast=3, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df
        self.__slow = slow
        self.__fast = fast
        self.__tipo = tipo
        self.__operaciones =  operatiOnOnActve( ticket = self.__ticket, tipo = self.__tipo )
        self.ejecutar()
        

    def ejecutar(self):

        ms = ma(self.__df, self.__slow, add=False) 
        mf = ma(self.__df, self.__fast, add=False)

        cruceUp=False
        
        for indice in range(self.__slow, len(mf)):
            if( mf.values[indice] > ms.values[indice] ):
                if( cruceUp == False):
                    cruceUp = True 
                    self.__operaciones.loadOperacion(self.__df.values[indice,0], self.__df.index[indice].to_pydatetime(),1, 'compra')

                    #operacion.loadOperacion(date = mf.index[indice].to_pydatetime(), typeOperacion= True, valorTicket = mf.values[indice] )

            if( mf.values[indice] < ms.values[indice] ):
                if( cruceUp == True ):
                    cruceUp = False
                    self.__operaciones.loadOperacion(self.__df.values[indice,0], self.__df.index[indice].to_pydatetime(),1, 'venta')
                    #operacion.loadOperacion(date = mf.index[indice].to_pydatetime(), typeOperacion= False, valorTicket = mf.values[indice] )

        if(self.__operaciones.getCantidadActivo() != 0 ):
            self.__operaciones.loadOperacion(self.__df.values[-1,0], self.__df.index[-1].to_pydatetime(), 1, 'venta')

    def getGanaciasNeta(self):
        #Incluye las comisiones
        return (round(self.__operaciones.getGananciaNeta(),2))

    def getAciertos(self, print_resultado=True):
        #determina la cantidad de operaciones exitosas ($venta > $compra)
        #Considerar comisiones
        resultado   = 0
        valorCompra = 0
        valorVenta  = 0

        if( print_resultado == True):
            print("\tListado de Aciertos")
        
        for p in self.__operaciones.getListOperacion():
            if( p.getTypeOperacion() == 'compra' ):
                #Egreso de dinero
                valorCompra = p.getCostoOperacionNeto()
                compra = p 
            else:
                #Venta de activo
                valorVenta = p.getCostoOperacionNeto()
                venta = p

                if( compra != None and venta != None):
                    valorCompra = compra.getCostoOperacionNeto()
                    valorVenta  = venta.getCostoOperacionNeto()
                    if( valorCompra < valorVenta ):
                        porcentual = ( (valorVenta - valorCompra ) / valorCompra ) * 100
                        resultado = resultado + porcentual
                        if( print_resultado == True):
                            print("\tCompra: " + str(compra.getDateTime().date()) + "\tValor: " + str(round(valorCompra,2))+ "\tVenta: " + str(venta.getDateTime().date()) + "\tValor: " + str(round(valorVenta,2)) + "\t Diferencia: " + str(round(porcentual,2)) + "%")
                    compra = None
                    venta = None
        return( resultado )

    def getFallas(self, print_resultado=True):
        #determina la cantidad de operaciones fallidas ($venta > $compra)
        #Considerar comisiones
        resultado   = 0
        valorCompra = 0
        valorVenta  = 0
        porcentual  = 0

        if(print_resultado == True):
            print("\tListado de Falla")
        
        for p in self.__operaciones.getListOperacion():
            if( p.getTypeOperacion() == 'compra' ):
                #Egreso de dinero
                compra = p 

            else:
                #Venta de activo
                venta = p
                
                if( compra != None and venta != None):
                    valorCompra = compra.getCostoOperacionNeto()
                    valorVenta  = venta.getCostoOperacionNeto()
                    if( valorCompra > valorVenta ):                       
                        porcentual = ( ( (valorVenta - valorCompra ) / valorCompra ) * 100 )
                        resultado += porcentual
                        
                        if( print_resultado == True):
                            print("\tCompra: " + str(compra.getDateTime().date()) + "\tValor: " + str(round(valorCompra,2))+ "\tVenta: " + str(venta.getDateTime().date()) + "\tValor: " + str(round(valorVenta,2)) + "\t Diferencia: " + str(round(porcentual,2)) + "%")
                    compra = None
                    venta = None

        return( resultado )

    def getGananciaPorcentual(self):
        resultado = 0
        valorIngreso =  self.__df.values[ 0, 0 ]
        resultado = (self.getGanaciasNeta() / valorIngreso ) * 100
        return ( round(resultado,2) ) 
    
    def get_day_in(self):
        return( self.__operaciones.get_day_in() )

class BuyAndHold():
    #Comprar y retener
    def __init__(self, ticket, df, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df['Close']
        self.__tipo = tipo
        self.__operaciones =  operatiOnOnActve( ticket = self.__ticket, tipo = self.__tipo )
        self.ejecutar()

    def ejecutar(self):
        self.__operaciones.loadOperacion(self.__df[ 0 ], self.__df.index[ 0 ].to_pydatetime(), 1, 'compra')
        self.__operaciones.loadOperacion(self.__df[-1 ], self.__df.index[-1 ].to_pydatetime(), 1, 'venta' )

    def getGanaciasNeta(self):
        #Incluye las comisiones
        return (round(self.__operaciones.getGananciaNeta(),2))     

    def getGananciaPorcentual(self):
        resultado = 0
        valorIngreso =  self.__df[ 0 ]
        resultado = (self.getGanaciasNeta() / valorIngreso ) * 100
        return (round(resultado,2)) 

    def get_day_in(self):
        return( self.__operaciones.get_day_in() )
        
class rsi_sobrecompra_sobreventa():
    #Utiliza limite de sobre compra y sobre venta para ejecutar la accion
    def __init__(self, ticket, df, rsi = 20, sobrecompra=(70/100), sobreventa=(30/100), tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df
        self.__rsi = rsi
        self.__sobrecompra = sobrecompra
        self.__sobreventa = sobreventa
        self.__tipo = tipo
        self.__operaciones =  operatiOnOnActve( ticket = self.__ticket, tipo = self.__tipo )
        self.ejecutar()
    
    def ejecutar(self):
        _rsi = rsi(self.__df, self.__rsi, add=False)

        comprado=False
        #print(self.__df[20:21])
        for p in range(self.__rsi, len(_rsi)):

            if( (_rsi[ p ] > self.__sobrecompra) and (comprado == False) ):
                comprado = True
                self.__operaciones.loadOperacion(self.__df['Close'].values[ p ], self.__df.index[ p ].to_pydatetime(),1, 'compra')
            if( (_rsi[ p ] < self.__sobreventa) and (comprado == True) ):
                comprado = False
                self.__operaciones.loadOperacion(self.__df['Close'].values[ p ], self.__df.index[ p ].to_pydatetime(),1, 'venta')
    
        if(self.__operaciones.getCantidadActivo() != 0 ):
            self.__operaciones.loadOperacion(self.__df['Close'].values[ p ], self.__df.index[ -1 ].to_pydatetime(),1, 'venta')
        
    def getGanaciasNeta(self):
        #Incluye las comisiones
        return (round(self.__operaciones.getGananciaNeta(),2))
    
    def getGananciaPorcentual(self):
        resultado = 0
        valorIngreso =  self.__df['Close'].values[ 0 ]
        resultado = (self.getGanaciasNeta() / valorIngreso ) * 100
        return (round(resultado,2)) 

    def get_day_in(self):
        return( self.__operaciones.get_day_in() )    


class rsi_media_ponderada():
    #Utiliza una señal cocodrillo sobre un rsi
    def __init__(self, ticket, df, rsi = 20, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df
        self.__rsi = rsi
        self.__tipo = tipo
        self.__operaciones =  operatiOnOnActve( ticket = self.__ticket, tipo = self.__tipo )
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
                        self.__operaciones.loadOperacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'compra')
                    
            if( mf.values[indice] < ms.values[indice] ):
                if( _rsi.values[i] > 0.2 ):  
                    if( cruceUp == True ):
                        cruceUp = False
                        self.__operaciones.loadOperacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'venta')
                
        if(self.__operaciones.getCantidadActivo() != 0 ):
            self.__operaciones.loadOperacion(self.__df.values[-1,0], self.__df.index[-1].to_pydatetime(), 1, 'venta')

    def getGanaciasNeta(self):
        #Incluye las comisiones
        return (round(self.__operaciones.getGananciaNeta(),2))  

    def getGananciaPorcentual(self):
        resultado = 0
        valorIngreso =  self.__df.values[0,0]
        resultado = (self.getGanaciasNeta() / valorIngreso ) * 100
        return (round(resultado,2)) 

    def get_day_in(self):
        return( self.__operaciones.get_day_in() )


class estrategia_rsi_media(operatiOnOnActve):
    def __init__(self, ticket, df, rsi = 20, tipo='accionbyma'):
        
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
                        super().loadOperacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'compra') 
                                            
            if( mf.values[indice] < ms.values[indice] ):
                if( _rsi.values[i] > 0.2 ):  
                    if( cruceUp == True ):
                        cruceUp = False
                        super().loadOperacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'venta')
                
        if(super().get_cantidad_activos() != 0 ):
            super().loadOperacion(self.__df.values[i,0], self.__df.index[i].to_pydatetime(),1, 'venta')
    