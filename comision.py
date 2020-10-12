
def comisionCedear():
    arancel = 0.6 / 100
    impuesto =  0.0968 / 100
    iva = (arancel * 0.21) + (impuesto * 0.21)
    return( arancel + impuesto + iva )    