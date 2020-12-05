import math
import datetime
from indicadores import *
from comision import *


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