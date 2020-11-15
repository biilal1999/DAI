from pickleshare import *

def loginBD(nombre, password):
    db = PickleShareDB('~/datos')
    coincide = False

    if nombre in db:
        if db[nombre]['password'] == password:
            coincide = True

    return coincide


def existeUsuario(nombre):
    db = PickleShareDB('~/datos')
    existe = False

    if nombre in db:
        existe = True

    return existe


def registrarse(nombre, password):
    exito = False

    if (existeUsuario(nombre) == False):
        db = PickleShareDB('~/datos')
        db[nombre] = dict()
        db[nombre]['password'] = password
        db[nombre] = db[nombre]
        exito = True

    return exito


def editarUsuario(nombreActual, nombreNuevo, password):
    editado = False

    if (existeUsuario(nombreNuevo) == False):
        db = PickleShareDB('~/datos')
        db[nombreNuevo] = dict()
        db[nombreNuevo]['password'] = password
        db[nombreNuevo] = db[nombreNuevo]
        del db[nombreActual]
        editado = True

    return editado
