import re


def comprobarCadena(cadena):
    res = re.match(r"[\w\s]+[A-Z]", cadena)

    return res


def comprobarCorreo(correo):
    res = re.match(r"^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,3})$", correo)

    return res


def comprobarTarjeta(tarjeta):
    res = re.match(r"^\d{4}([\ -]?)\d{4}\1\d{4}\1\d{4}$", tarjeta)

    return res


