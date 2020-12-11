import math
import datetime
from indicadores import *
from operacion import *
import pandas as pd   

"""
class DatoOperacion():
    def __init__(self, date, typeOperacion=True, valorTicket = 0, cantidad = 1, interesPorcentual = 1):
        self.__date=date
        self.__cantidad = cantidad
        #Tipo de operacion = True (es compra). False = venta
        self.__typeOperacion=typeOperacion
        self.__valorTicket=valorTicket
        self.__interesPorcentual=interesPorcentual

    def getDate(self):
        return self.__date
    def getTypeOperacion(self):
        return self.__typeOperacion
    def getValorTicket(self):
        return self.__valorTicket
    def getIntresPorcentual(self):
        return self.__interesPorcentual
    def getCantidad(self):
        return self.__cantidad

    def getCostoOperacionNeto(self):
        if(self.__typeOperacion == True):
            #Operacion de compra del instrumento
            return self.__valorTicket * self.__cantidad * (1+ self.__interesPorcentual )
        
        #Operacion de venta
        return self.__valorTicket * self.__cantidad * (1 - self.__interesPorcentual )
    
    def getCostoOperacionBruto(self):
        if(self.__typeOperacion == True):
            #Operacion de compra del instrumento
            return self.__valorTicket * self.__cantidad
        
        #Operacion de venta
        return self.__valorTicket * self.__cantidad

class Operacion():
    def __init__(self, interesPorcentual=1):
        self.__datoOperacion = []
        self.__interesPorcentual = interesPorcentual
    
    def loadOperacion(self, date, typeOperacion=True, valorTicket = 0, cantidad = 1 ):
        operacion = DatoOperacion(date, typeOperacion, valorTicket, cantidad, interesPorcentual = self.__interesPorcentual )
        self.__datoOperacion.append(operacion)
        
        if( typeOperacion == True ):
            tipo = "Compra"
        else:
            tipo = "Venta"
        
       # print("Tipo: " + tipo + "\tValor: " + str(round(valorTicket,2)) + "USD. \tFecha: " + str(date) )


    def getCntOperaciones(self):
        return(len(self.__datoOperacion))
    
    def getGananciaBruto(self):
        #sin considerar comisiones
        resultado = 0
        cantDisponible = 0

        for operacion in self.__datoOperacion:
            if(operacion.getTypeOperacion() == True):
                #Compra de instrumento
                cantDisponible += operacion.getCantidad()
                #Egreso de dinero
                resultado += (operacion.getCostoOperacionBruto() * (-1))
            else:
                #venta de instrumento
                cantDisponible -= operacion.getCantidad()
                #Ingreso de dinero
                resultado += operacion.getCostoOperacionBruto()
        
        return( round(resultado,2) )
    
    def getGananciaNeto(self):
        #Considerar comisiones
        resultado = 0

        for operacion in self.__datoOperacion:
            if(operacion.getTypeOperacion() == True):
                #Egreso de dinero
                resultado += (operacion.getCostoOperacionNeto() * (-1))
            else:
                #Ingreso de dinero
                resultado += operacion.getCostoOperacionNeto()    

        return( round(resultado,2) )

    def getGananciaPorcentaje(self):
         #Considerar comisiones
        resultado = 0
        valorCompra = 0
        valorVenta = 0
        for operacion in self.__datoOperacion:

            if(operacion.getTypeOperacion() == True):
                #Egreso de dinero
                valorCompra = operacion.getCostoOperacionNeto()
            else:
                #Ingreso de dinero
                valorVenta = operacion.getCostoOperacionNeto()
                if( valorCompra != 0):
                    porcentajeOperacion = (valorVenta - valorCompra) * 100 / valorCompra
                else:
                    print("Se intenta dividir por cero")
                resultado += porcentajeOperacion

        return( round(resultado,2) )    

    def getFallas(self):
        #determina la cantidad de operaciones fallidas ($venta > $compra)
        #Considerar comisiones
        resultado = 0
        valorCompra = 0
        valorVenta = 0

        print("Listado de Falla")
        for operacion in self.__datoOperacion:
            if(operacion.getTypeOperacion() == True):
                #Egreso de dinero
                valorCompra = operacion.getValorTicket()
            else:
                #Venta de activo
                valorVenta = operacion.getValorTicket()
                
                if( valorCompra > valorVenta ):
                    resultado += 1
                    porcentual = ((valorCompra - valorVenta ) / valorCompra ) * 100
                    print("\tFecha: " + str(operacion.getDate()) + "\tCompra: " + str(round(valorCompra,2))+ "\tVenta: " +str(round(valorVenta,2)) + "\t Diferencia: " + str(round(porcentual,2)) + "%")

        return( round(resultado,2) )

    def getAciertos(self):
        #determina la cantidad de operaciones fallidas ($venta > $compra)
        #Considerar comisiones
        resultado = 0
        valorCompra = 0
        valorVenta = 0

        print("Listado de Aciertos")
        for operacion in self.__datoOperacion:
            if(operacion.getTypeOperacion() == True):
                #Egreso de dinero
                valorCompra = operacion.getValorTicket()
            else:
                #Venta de activo
                valorVenta = operacion.getValorTicket()
                
                if( valorCompra < valorVenta ):
                    resultado += 1
                    porcentual = ((valorVenta - valorCompra ) / valorCompra ) * 100
                    print("\tFecha: " + str(operacion.getDate()) + "\tCompra: " + str(round(valorCompra,2))+ "\tVenta: " +str(round(valorVenta,2)) + "\t Diferencia: " + str(round(porcentual,2)) + "%")

        return( round(resultado,2) )

def cocodrillo(ticket, slow=21, fast=3):
    try:
        operacion = Operacion(interesPorcentual = comisionCedear() )

        ms = ma(ticket, slow, add=False) 
        mf = ma(ticket, fast, add=False)
       
        cruceUp=False
        
        for indice in range(slow, len(mf)):

            if( mf[indice] > ms[indice] ):
                if( cruceUp == False):
                    cruceUp = True                
                    operacion.loadOperacion(date = mf.index[indice].to_pydatetime(), typeOperacion= True, valorTicket = mf.values[indice] )

            if( mf[indice] < ms[indice] ):
                if( cruceUp == True ):
                    cruceUp = False
                    operacion.loadOperacion(date = mf.index[indice].to_pydatetime(), typeOperacion= False, valorTicket = mf.values[indice] )
    except:
        print("Salta una excepcion")
    
    return( operacion )
"""
class Cocodrilo():
    def __init__(self, ticket, df, slow=21, fast=3, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df['Close']
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
        
            if( mf[indice] > ms[indice] ):
                if( cruceUp == False):
                    cruceUp = True 
                    self.__operaciones.loadOperacion(self.__df.values[indice], self.__df.index[indice].to_pydatetime(),1, 'compra')

                    #operacion.loadOperacion(date = mf.index[indice].to_pydatetime(), typeOperacion= True, valorTicket = mf.values[indice] )

            if( mf[indice] < ms[indice] ):
                if( cruceUp == True ):
                    cruceUp = False
                    self.__operaciones.loadOperacion(self.__df.values[indice], self.__df.index[indice].to_pydatetime(), 1, 'venta')
                    #operacion.loadOperacion(date = mf.index[indice].to_pydatetime(), typeOperacion= False, valorTicket = mf.values[indice] )

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

        return( round(resultado,2) )
    
    def getFallas(self, print_resultado=True):
        #determina la cantidad de operaciones fallidas ($venta > $compra)
        #Considerar comisiones
        resultado = 0
        valorCompra = 0
        valorVenta = 0

        if(print_resultado == True):
            print("\tListado de Falla")
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
                    if( valorCompra > valorVenta ):
                        porcentual = ( (valorVenta - valorCompra ) / valorCompra ) * 100
                        resultado = resultado + porcentual
                        if( print_resultado == True):
                            print("\tCompra: " + str(compra.getDateTime().date()) + "\tValor: " + str(round(valorCompra,2))+ "\tVenta: " + str(venta.getDateTime().date()) + "\tValor: " + str(round(valorVenta,2)) + "\t Diferencia: " + str(round(porcentual,2)) + "%")
                    compra = None
                    venta = None

        return( round(resultado,2) )

    def getGananciaPorcentual(self):
        return( round(self.getAciertos(False) + self.getFallas(False),2))


class BuyAndHold():
    #Comprar y retener
    def __init__(self, ticket, df, tipo='accionbyma'):
        self.__ticket = ticket 
        self.__df = df['Close']
        #print( type( self.__df ) )
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
        
        
       # nd = self.__df[-2:]
       # print(  nd )
       # print(  nd.iloc[-1].to_pydatetime()  )
       # print(  nd.iloc[0,-1]  )