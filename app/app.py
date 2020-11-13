# ./app/app.py

from flask import (Flask, url_for, redirect, render_template, session)
from pickleshare import *
from matrices import *
from criba import *
from fibonacci import *
from balanceo import *
from expresiones import *
from svg import *
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html')


@app.route('/ejercicio1')
def ejercicio1():
   return render_template('ejercicio1.html')


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


@app.route('/expresiones')
def expresionesError():
    cadena = '<h2>Debe especificar qué expresion regular debe comprobar, de la siguiente forma: </h2>'
    cadena += '<ul>'
    cadena += '<li><strong>localhost:5000/expresiones/frase/<cad></strong> Cuando es una frase</li>'
    cadena += '<li><strong>localhost:5000/expresiones/correo/<correo></strong> Cuando es un correo electrónico</li>'
    cadena += '<li><strong>localhost:5000/expresiones/tarjeta/<tarjeta></strong> Cuando es una tarjeta de crédito</li>'
    cadena += '</ul>'

    return cadena


@app.route('/expresiones/frase')
def cadenaError():
    cadena = '<h2>Debe especificar una cadena de texto en la URL</h2>'

    return cadena

@app.route('/expresiones/correo')
def correoError():
    cadena = '<h2>Debe especificar un correo electrónico en la URL</h2>'

    return cadena

@app.route('/expresiones/tarjeta')
def tarjetaError():
    cadena = '<h2>Debe especificar una tarjeta de crédito en la URL</h2>'

    return cadena

@app.route('/expresiones/frase/<cad>')
def cadenaComprobacion(cad):
    resultado = comprobarCadena(cad)
    frase = ""

    if resultado != None:
       frase = '<h2>La cadena es correcta</h2>'

    else:
       frase = '<h2>La cadena es incorrecta</h2>'

    return frase


@app.route('/expresiones/correo/<correo>')
def correoComprobacion(correo):
    resultado = comprobarCorreo(correo)
    frase = ""

    if resultado != None:
       frase = '<h2>El correo electrónico es correcto</h2>'

    else:
       frase = '<h2>El correo electrónico es incorrecto</h2>'

    return frase


@app.route('/expresiones/tarjeta/<tarjeta>')
def tarjetaComprobacion(tarjeta):
    resultado = comprobarTarjeta(tarjeta)
    frase = ""

    if resultado != None:
       frase = '<h2>La tarjeta de crédito es correcta</h2>'

    else:
       frase = '<h2>La tarjeta de crédito es incorrecta</h2>'

    return frase


@app.route('/svg')
def opcional():
    formas = ['circle', 'ellipse', 'line']
    colores = ['darkmagenta', 'dodgerblue', 'lightcoral', 'olivedrab', 'gold', 'darkcyan', 'oldlace']

    cadena = pintarSVG(formas, colores)

    return cadena


@app.errorhandler(404)
def paginaNoEncontrada(error):
    cadena = '<h1> PÁGINA NO ENCONTRADA. POR FAVOR, REVISE SU DIRECCIÓN URL</h1>'

    return cadena
