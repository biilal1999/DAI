import string
import random

def generadorCadenas():
    num = random.randrange(2, 14)
    string.letters = '[]'
    cad = random.choice(string.letters)

    for i in range(num-1):
        cad += random.choice(string.letters)

    return cad


def comprobarBalanceo(cadena):
    res = True
    contadorAbiertos = 0
    contadorCerrados = 0

    while res == True:
        for i in cadena:
            if i == '[':
                contadorAbiertos += 1
            else:
                contadorCerrados += 1

            if contadorCerrados > contadorAbiertos:
                res = False
            
                return res
         
        res = False

    if contadorAbiertos != contadorCerrados:
        res = False

    else:
        res = True

    return res

