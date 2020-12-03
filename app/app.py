# ./app/app.py

from flask import (Flask, url_for, redirect, render_template, session, request, flash, jsonify)
from pickleshare import *
from matrices import *
from criba import *
from fibonacci import *
from balanceo import *
from expresiones import *
from svg import *
from model import *
from pymongo import MongoClient
from bson import ObjectId
from random_object_id import generate
app = Flask(__name__)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


client = MongoClient("mongo", 27017)
db = client.SampleCollections

paginas = []
base = "samples_pokemon"

#paginas = "hola"
#if 'paginas' in session:
# return request.path

def actualizarPaginas():
    ruta = str(request.path)
    paginas.append(ruta)

    if len(paginas) > 3:
        paginas.pop(0)


@app.route('/')
@app.route('/index')
def index():
   actualizarPaginas()
   return render_template('index.html', paginas=paginas)



@app.route('/api/pokemons', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        lista = []
        pok = db[base].find().sort('name')

        for p in pok:
            lista.append({
                'id':   str(p.get('_id')),
                'name': p.get('name'),
                'height': p.get('height'),
                'weight': p.get('weight')
            })

        return jsonify(lista)

    elif request.method == 'POST':
        nombre = "Sin nombre"
        height = "2.0 m"
        weight = "10.0 kg"

        if 'name' in request.form:
            nombre = request.form['name']

        if 'height' in request.form:
            height = request.form['height']

        if 'weight' in request.form:
            weight = request.form['weight']

        id = generate()

        myquery = { "_id": id, "name": nombre, "height": height, "weight": weight }
        db[base].insert_one(myquery)

        return jsonify(myquery)



@app.route('/mongo', methods=['GET', 'POST'])
def mongo():
    tag = ""

    if request.method != 'POST':
        actualizarPaginas()
        return render_template('lista.html', paginas=paginas, tag=tag)

    else:

        if 'pok' in request.form:
            nuevoNombre = request.form['pok']
            todos = db[base].find()
            id = -1.0

            for p in todos:
                id = p['id']

            id = id + 1.0
            myquery = { "name": nuevoNombre, "id": id }
            db[base].insert_one(myquery)
            flash("Pokemon añadido con éxito")

            return render_template('lista.html', paginas=paginas, tag=tag)

        if 'idenobj' in request.form:
            idenobj = request.form['idenobj']
            idenobj = float(idenobj)
            nombre = request.form['nombre']
            antiguo = { "id": idenobj }
            nuevo = { "$set": { "name": nombre } }
            db[base].update_one(antiguo, nuevo)
            flash("Pokemon actualizado con éxito")

            return render_template('lista.html', paginas=paginas, tag=tag)

        tag = "res"

        if 'nombre' in request.form:
            nombre = request.form['nombre']

        if 'id' in request.form:
            id = request.form['id']

            if id != '':
                id = int(id)
                id = id * 1.0

        else:
            id = -1.0

        vec = db[base].find()
        lista = []

        for obj in vec:
            if nombre in obj['name'] or obj['id'] == id:
                lista.append(obj)

        return render_template('lista.html', lista=lista, paginas=paginas, tag=tag)


@app.route('/acciones', methods=['GET', 'POST'])
def baseDatos():
    tag = ""

    if request.method == 'POST':
        accion = request.form['accion']
        iden = request.form['identificador']
        iden = float(iden)

        if accion == "borrar":
            myquery = {'id': iden}
            flash("Pokémon borrado correctamente")
            db[base].delete_one(myquery)

        if accion == "editar":
            tag="mod"
            myquery = {'id': iden}
            obj = db[base].find_one(myquery)
            valor = obj['name']
            return render_template('lista.html', paginas=paginas, tag=tag, valor=valor, iden=iden)

    return render_template('lista.html', paginas=paginas)


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

   cadena = cadena + '<h2>Cadena ordenada: ' + str(primeraLista) + '</h2>'

   segundaLista = lista.split(',')
   cadena = cadena + '<h2> Ordenación con selección: '
   app.logger.debug(segundaLista)
   tinicio = time.time()
   seleccion(segundaLista)
   tfinal = time.time()
   t = str(tfinal - tinicio)
   cadena = cadena + t + ' segundos</h2>'

   cadena = cadena + '<h2>Cadena ordenada: ' + str(segundaLista) + '</h2>'

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

   return '<h2>Primos anteriores: ' + cad + ' </h2>'


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



@app.route('/login', methods=['GET', 'POST'])
def funcionLogin():
    actualizarPaginas()
    tag = ""

    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['pass']

        if loginBD(username, password) == True:
            session['usuario'] = username
            session['password'] = password
            flash('Inicio de sesión correcto! Bienvenido a nuestra web')
            return redirect(url_for('index'))

        else:
            tag="Usuario o contraseña incorrectos"
            return render_template('login.html', tag=tag, paginas=paginas)
    else:
        return render_template('login.html', tag=tag, paginas=paginas)


@app.route('/logout')
def funcionLogout():
    flash('Ha cerrado su sesión. Nos vemos!')
    session.pop('usuario', None)
    session.pop('password', None)

    return redirect(url_for('index'))


@app.route('/registro', methods=['GET', 'POST'])
def funcionRegistro():
    actualizarPaginas()
    tag = ""

    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['pass']

        if registrarse(username, password) == True:
            session['usuario'] = username
            session['password'] = password
            flash('Se ha registrado correctamente! Bienvenido a nuestra web')
            return redirect(url_for('index'))

        else:
            tag="El nombre de usuario no está disponible"
            return render_template('registro.html', tag=tag, paginas=paginas)

    else:
        return render_template('registro.html', tag=tag, paginas=paginas)


@app.route('/miperfil')
def miPerfil():
    accion="ver"

    if 'usuario' not in session:
        return redirect(url_for('login'))

    else:
        actualizarPaginas()

        return render_template('user.html', paginas=paginas, accion=accion)


@app.route('/editarperfil', methods=['GET', 'POST'])
def editarPerfil():
    tag = ""
    accion="editar"

    if 'usuario' not in session:
        return redirect(url_for('login'))

    else:
        actualizarPaginas()

        if request.method == 'POST':
            username = request.form['usuario']
            password = request.form['pass']

            if editarUsuario(session['usuario'], username, password) == True:
                flash('Se han editado sus datos correctamente')
                session['usuario'] = username
                session['password'] = password
                return redirect(url_for('miPerfil'))

            else:
                tag="El nombre de usuario ya está siendo utilizado"
                return render_template('user.html', tag=tag, paginas=paginas, accion=accion)

        else:
            return render_template('user.html', paginas=paginas, accion=accion)


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
