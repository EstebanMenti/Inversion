import math
import datetime as date
#from indicadores import *
from comision import *


class operacion():
    def __init__(self, ticket, valorTicket, datetime,   cantidad = 1, typeOperacion = 'compra', tipo = 'accionbyma' ):
        self.__ticket = ticket
        self.__valorTicket = valorTicket
        self.__datetime = datetime
        self.__cantidad = cantidad
        if(typeOperacion.lower() == 'compra' or typeOperacion.lower() == 'venta'):
            self.__typeOperacion = typeOperacion.lower()
        else:
            self.__typeOperacion = 'compra'
            print('****** EXCEPCION ******')        
        self.__comision = calculoComision(valorTicket, cantidad, tipo )

    def getTicket(self):
        return self.__ticket
    def getCantidad(self):
        return self.__cantidad
    def getTypeOperacion(self):
        return self.__typeOperacion
    def getValorTicket (self):
        return self.__valorTicket
    def getDateTime(self):
        return self.__datetime
    def getComision(self):
        return self.__comision
    def getCostoOperacionNeto(self):
        if(self.__typeOperacion == 'compra'):
            #Operacion de compra del instrumento
            return self.getCostoOperacionBruto() + self.getComision()
        #Operacion de venta
        return self.getCostoOperacionBruto() - self.getComision()    
    def getCostoOperacionBruto(self):
        #Operacion sin comisiones
        return self.getValorTicket() * self.getCantidad()

class operatiOnOnActve():
    def __init__(self, ticket, tipo='accionbyma'):
         self.__ticket = ticket
         self.__tipo = tipo.lower() 
         self.__datoOperacion = []
    def loadOperacion(self, valorTicketq, datetime=date.date.today(), cantidad=1, typeOperacion='compra' ):
        p = operacion(self.__ticket, valorTicketq, datetime, cantidad, typeOperacion, tipo = self.__tipo )
        self.__datoOperacion.append(p)
    def getTicket(self):
        return self.__ticket    
    def getCantidadActivo(self):
        print("obtiene la cantidad de papeles que se tiene (Ej: se compran 4, se venten 1, resultado: 3")
        cnt = 0
        for i in self.__datoOperacion:
            if(i.getTypeOperacion() == 'compra'):
                cnt = cnt + i.getCantidad()
            else:
                cnt = cnt - i.getCantidad()
        return cnt
    def getCantidadOperacion(self):
        return len(self.__datoOperacion)
    def getGananciaBruto(self):
        #retorna el valor de las operaciones sin las comisiones
        resultado = 0                   #Dinero puesto

        for i in self.__datoOperacion:
            if( i.getTypeOperacion == 'compra' ): 
                resultado = resultado - i.getCostoOperacionBruto() #dinero gastado 
            else:
                resultado = resultado + i.getCostoOperacionBruto() #dinero obtenido

        return resultado
    def getGananciaNeta(self):
        #retorna el valor de las operaciones con las comisiones incluidas
        resultado = 0

        for i in self.__datoOperacion:
            if( i.getTypeOperacion() == 'compra' ): 
                resultado -= (i.getCostoOperacionNeto() * +1)           #dinero gastado
            else:
                resultado = resultado + i.getCostoOperacionNeto()       #dinero obtenido
        return resultado
    def getListOperacion(self):
        #retorna el listado de operaciones realizadas
        return self.__datoOperacion
    
