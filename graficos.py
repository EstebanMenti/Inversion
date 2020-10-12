import mplfinance as mpf
import matplotlib.pyplot as plt 

def grafico_vela(ticket):
    mpf.plot(ticket, type='candle', volume=True)

#No esta funcionando
def grafico_cierre(ticket):
    fig = plt.figure(figsize=(16,8))
    plt.subplot(2,1,1)
    plt.plot( ticket[['Close']] )
    #plt.axhline(y=0, color='r')
    plt.title("Precio de cierre")
    plt.subplot(2,1,2)
    plt.plot( ticket[['MA_50']] )
    plt.title("MA_50")
    plt.show()