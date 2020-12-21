
def comisionCedear():
    arancel = 0.6 / 100
    impuesto =  0.0968 / 100
    iva = (arancel * 0.21) + (impuesto * 0.21)
    return( arancel + impuesto + iva )    

def calculoComision(valorTicket, cantidad = 1, tipo='accionbyma'):
    #Determina la comision de lo que se compre
    resultado = 0

    if(tipo.lower() == 'accionbyma' or tipo.lower() == 'cedear'):
        arancel = ( 0.6 / 100 ) * valorTicket * cantidad
        impuesto =  (0.0968 / 100) * valorTicket * cantidad
        iva = (arancel * 0.21) + (impuesto * 0.21)
        resultado = arancel + impuesto + iva

    return( resultado )
