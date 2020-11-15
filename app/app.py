# ./app/app.py

from flask import (Flask, url_for, redirect, render_template, session, request)
from pickleshare import *
from matrices import *
from criba import *
from fibonacci import *
from balanceo import *
from expresiones import *
from svg import *
from data/model import *
app = Flask(__name__)


app.secret_key = 'mi clave'

paginas = []

#paginas = "hola"
#if 'paginas' in session:
# return request.path

def actualizarPaginas():
    if 'paginas' in session:
        ruta = str(request.path)
        paginas.append(ruta)

        if len(paginas) > 3:
            paginas.pop(0)


@app.route('/')
@app.route('/index')
def index():
   actualizarPaginas()
   return render_template('index.html', paginas=paginas)


@app.route('/ejercicio1')
def ejercicio1():
   actualizarPaginas()
   return render_template('ejercicio1.html', paginas=paginas)


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


@app.route('/ordenaEjercicio')
def ejercicioOrdenaFormulario():
    actualizarPaginas()
    return render_template('ejercicio1.html', mensaje="Introduzca números separados por comas", formulario="si", ruta="../ordenaEjercicioResuelto", paginas=paginas)


@app.route('/ordenaEjercicioResuelto', methods=['GET'])
def ejercicioOrdena():
    tag=""

    if request.args.get('datos') == "":
        return render_template('ejercicio1.html',mensaje="Introduzca números separados por comas" ,formulario="si", tag=tag, paginas=paginas)

    else:
        cad = ordena(request.args.get('datos'))
        tag="res"

        return render_template('ejercicio1.html',mensaje="Introduzca números separados por comas", formulario = "si",tag=tag, cadena = cad, paginas=paginas)


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


@app.route('/cribaEjercicio')
def ejercicioCribaFormulario():
    actualizarPaginas()
    return render_template('ejercicio1.html', mensaje="Introduzca un número", formulario="si", ruta="../cribaEjercicioResuelto", paginas=paginas)


@app.route('/cribaEjercicioResuelto', methods=['GET'])
def ejercicioCriba():
    tag=""

    if request.args.get('datos') == "":
        return render_template('ejercicio1.html', mensaje="Introduzca un número", formulario="si", tag=tag, paginas=paginas)

    else:
        cad = cribaEras(request.args.get('datos'))
        tag="res"

        return render_template('ejercicio1.html', mensaje="Introduzca un número", formulario="si", tag=tag, cadena=cad, paginas=paginas)


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


@app.route('/fibonacciEjercicio')
def ejercicioFibonacci():
    actualizarPaginas()
    num = fibonacci()

    return render_template('ejercicio1.html', titulo="Fibonacci", nombre="Sucesión de Fibonacci", cadena = num, paginas=paginas)


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


@app.route('/balanceoEjercicio')
def ejercicioBalanceo():
    actualizarPaginas()
    cad = balancearCadenas()

    return render_template('ejercicio1.html', titulo = "Balanceo", nombre="Balanceo de cadenas", cadena = cad, paginas=paginas)


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


@app.route('/fraseEjercicio')
def ejercicioFraseFormulario():
    actualizarPaginas()
    return render_template('ejercicio1.html', mensaje="Introduzca una frase", formulario="si", ruta="../fraseEjercicioResuelto", paginas=paginas)


@app.route('/fraseEjercicioResuelto', methods=['GET'])
def ejercicioFrase():
    tag=""

    if request.args.get('datos') == "":
        return render_template('ejercicio1.html', mensaje="Introduzca una frase", formulario="si", tag=tag, paginas=paginas)

    else:
        cad = cadenaComprobacion(request.args.get('datos'))
        tag="res"

        return render_template('ejercicio1.html', mensaje="Introduzca una frase", formulario="si", tag=tag, cadena=cad, paginas=paginas)


@app.route('/expresiones/correo/<correo>')
def correoComprobacion(correo):
    resultado = comprobarCorreo(correo)
    frase = ""

    if resultado != None:
       frase = '<h2>El correo electrónico es correcto</h2>'

    else:
       frase = '<h2>El correo electrónico es incorrecto</h2>'

    return frase


@app.route('/correoEjercicio')
def ejercicioCorreoFormulario():
    actualizarPaginas()
    return render_template('ejercicio1.html', mensaje="Introduzca un correo electrónico", formulario="si", ruta="../correoEjercicioResuelto", paginas=paginas)


@app.route('/correoEjercicioResuelto', methods=['GET'])
def ejercicioCorreo():
    tag=""

    if request.args.get('datos') == "":
        return render_template('ejercicio1.html', mensaje="Introduzca un correo electrónico", formulario="si", tag=tag, paginas=paginas)

    else:
        cad = correoComprobacion(request.args.get('datos'))
        tag="res"

        return render_template('ejercicio1.html', mensaje="Introduzca un correo electrónico", formulario="si", tag=tag, cadena=cad, paginas=paginas)


@app.route('/expresiones/tarjeta/<tarjeta>')
def tarjetaComprobacion(tarjeta):
    resultado = comprobarTarjeta(tarjeta)
    frase = ""

    if resultado != None:
       frase = '<h2>La tarjeta de crédito es correcta</h2>'

    else:
       frase = '<h2>La tarjeta de crédito es incorrecta</h2>'

    return frase


@app.route('/tarjetaEjercicio')
def ejercicioTarjetaFormulario():
    actualizarPaginas()
    return render_template('ejercicio1.html', mensaje="Introduzca una tarjeta de crédito", formulario="si", ruta="../tarjetaEjercicioResuelto", paginas=paginas)


@app.route('/tarjetaEjercicioResuelto', methods=['GET'])
def ejercicioTarjeta():
    tag=""

    if request.args.get('datos') == "":
        return render_template('ejercicio1.html', mensaje="Introduzca una tarjeta de crédito", formulario="si", tag=tag, paginas=paginas)

    else:
        cad = tarjetaComprobacion(request.args.get('datos'))
        tag="res"

        return render_template('ejercicio1.html', mensaje="Introduzca una tarjeta de crédito", formulario="si", tag=tag, cadena=cad, paginas=paginas)



@app.route('/login')
def funcionLogin():
    return render_template('login.html')


@app.route('/svg')
def opcional():
    formas = ['circle', 'ellipse', 'line']
    colores = ['darkmagenta', 'dodgerblue', 'lightcoral', 'olivedrab', 'gold', 'darkcyan', 'oldlace']

    cadena = pintarSVG(formas, colores)

    return cadena


@app.route('/svgEjercicio')
def ejercicioSVG():
    actualizarPaginas()
    cad = opcional()

    return render_template('ejercicio1.html', titulo = "SVG", nombre="FIGURAS SVG", cadena = cad, paginas=paginas)


@app.errorhandler(404)
def paginaNoEncontrada(error):
    cadena = '<h1> PÁGINA NO ENCONTRADA. POR FAVOR, REVISE SU DIRECCIÓN URL</h1>'

    return cadena
