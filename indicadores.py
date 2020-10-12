import os
import pandas as pd #pip install pandas

#Determina la media movil de "n" ruedas
def ma(ticket, n, add=True):
    try:
        ma=pd.Series(pd.Series.rolling(ticket['Close'],n).mean(), name='MA_' + str(n))
    except:
        print("Excepcion capturada en def ma(ticket, n, add=True) ")
    if(add == True):
        ticket = ticket.join(ma)
    else:
        ticket = ma
    return ticket

#Caclula la media movil ponderada de "n" ruedas. "add" lo agrega en los mismo datos
def ema(ticket, n, add=True):
    try:
        ema = pd.Series(pd.Series.ewm(ticket['Close'], span = n, min_periods = n -1, adjust = False).mean(), name='EMA_' + str(n))
    except:
       print("Excepcion capturada en def ema(ticket, n, add=True)") 
    if(add == True):
        ticket = ticket.join(ema)
    else:
        ticket = ema
    return ticket

#indice de fuerza relativa
def rsi(ticket, n, add=True):
    i = 0
    upi=[0]
    doi=[0]
    ticket=ticket.reset_index()

    while( i + 1 <= ticket.index[-1]):
        upMove = ticket['High'].values[i + 1] - ticket['High'].values[i ]
        downMove = ticket['Low'].values[i] - ticket['Low'].values[i + 1]

        if( upMove > downMove and upMove > 0):
            upD = upMove
        else:
            upD = 0
        upi.append(upD)
        
        if( downMove > upMove and downMove > 0):
            dod = downMove
        else:
            dod = 0
        doi.append(dod)

        i = i + 1
    
    upi = pd.Series(upi)
    doi = pd.Series(doi)
    posdi = pd.Series(pd.Series.ewm(upi, span=n, min_periods= n -1).mean())
    negdi = pd.Series(pd.Series.ewm(doi, span=n, min_periods= n -1).mean())
    rsi = pd.Series(posdi /(posdi + negdi), name= 'RSI_' + str(n))
    
    if(add == True):
        ticket = ticket.join(rsi)
        ticket.set_index('Date', inplace=True)
    else:
        ticket = rsi
    return(ticket)
