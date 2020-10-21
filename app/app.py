# ./app/app.py

from flask import Flask
from matrices import *
from criba import *
from fibonacci import *
from balanceo import *
app = Flask(__name__)


@app.route('/')
def hello_world():
   return 'Hello, World!'


@app.route('/ordena')
def errorOrdena():
   cadena = '<h2>Debe introducir los números de la lista en la URL para poder acceder</h2>'

   return cadena

@app.route('/ordena/<lista>')                                                                   
def ordena(lista):
   primeraLista = lista.split(',')
   cadena = '<h2> Ordenación en burbuja: '
   app.logger.debug(primeraLista)
   tinicio = time.time()
   ordenamientoBurbuja(primeraLista)
   tfinal = time.time()
   t = str(tfinal - tinicio)
   cadena = cadena + t + ' segundos</h2>'

   cadena = cadena + '<h3>Cadena ordenada: ' + str(primeraLista) + '</h3>'

   segundaLista = lista.split(',')
   cadena = cadena + '<h2> Ordenación con selección: '
   app.logger.debug(segundaLista)
   tinicio = time.time()
   seleccion(segundaLista)
   tfinal = time.time()
   t = str(tfinal - tinicio)
   cadena = cadena + t + ' segundos</h2>'

   cadena = cadena + '<h3>Cadena ordenada: ' + str(segundaLista) + '</h3>'

   return cadena


@app.route('/criba')
def cribaError():
   cadena = '<h2>Debe introducir un número en la URL para poder acceder</h2>'

   return cadena


@app.route('/criba/<n>')
def cribaEras(n):
   numero = int(n)
   lista = list(range(2, numero+1))
   criba(lista, numero)
   cad = str(lista)
   
   return '<h3>Primos anteriores: ' + cad + ' </h3>'


@app.route('/fibonacci')
def fibonacci():
    f = open("numero.txt")
    dato = f.read()
    f.close()
    dato = int(dato)
    dato = fib(dato)

    f = open("resultado.txt", "w")
    dato = str(dato)
    f.write(dato)
    f.close()

    f = open("resultado.txt")
    numero = f.read()
    f.close()

    return numero


@app.route('/balanceo')
def balancearCadenas():
    lista = generadorCadenas()
    resultado = comprobarBalanceo(lista)

    if resultado == True:
        palabra = "correcto"

    elif resultado == False:
        palabra = "incorrecto"

    cadena = '<h2>La cadena es ' + lista + ' </h2>'
    cadena = cadena + '<h2>El balanceo es ' + palabra + ' </h2>'
    
    return cadena


#@app.route('/expresiones/palabra/<cadena>')
#def encontrarPalabra(cadena):
    
