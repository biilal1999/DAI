from pickleshare import *

def loginBD(nombre, password):
    db = PickleShareDB('data/datos.dat')
    coincide = False

    if nombre in db:
        if db[nombre].get('password') == password:
            coincide = True

    return coincide


def existeUsuario(nombre):
    db = PickleShareDB('data/datos.dat')
    existe = False

    if nombre in db:
        existe = True

    return existe


def registrarse(nombre, password):
    exito = False

    if (existeUsuario(nombre) == False):
        db = PickleShareDB('data/datos.dat')
        db[nombre] = dict()
        db[nombre]['password'] = password
        db[nombre] = db[nombre]
        exito = True

    return exito


def editarUsuario(nombreActual, nombreNuevo, password):
    editado = False

    if existeUsuario(nombreNuevo) == False:
        db = PickleShareDB('data/datos.dat')
        db[nombreNuevo] = dict()
        db[nombreNuevo]['password'] = password
        db[nombreNuevo] = db[nombreNuevo]
        del db[nombreActual]
        editado = True

    return editado
