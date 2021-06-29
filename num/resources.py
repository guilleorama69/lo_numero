import functools
from app import mysql
from flask import request, flash, session, redirect, url_for, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_socketio import disconnect


def on_login():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, pass, id FROM users WHERE mail = %s', [
                   email])
    user = cursor.fetchone()
    cursor.close()
    if user:
        if check_password_hash(user[1], password):
            return user
    else:
        return False


def create_user(email, name, lastname, password, birthday, gender):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (mail, name, last_name, pass, birthday, gender) VALUES (%s,%s,%s,%s,%s,%s)',
                       (email, name, lastname, generate_password_hash(password), birthday, gender))
        mysql.connection.commit()
        cursor.close()
        flash('Usuario creado correctamente')
    except:
        return flash('Ocurrio un error creando el usuario')


def exists_mail(mail):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT mail FROM users WHERE mail = %s', [mail])
    data = cursor.fetchone()
    cursor.close()
    if data:
        return True
    else:
        return False

 # Decoradores para autentificar


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_routes.login'))

        return view(**kwargs)

    return wrapped_view


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if g.user is None:
            flash('No auth')
            disconect()
            return
        else:
            return f(*args, **kwargs)

    return wrapped

    # Logica del Juego


def numeroOK(numeros):
    error = ""
    try:
        if len(str(numeros)) != 4:
            error = "Ingrese 4 digitos enteros"
            return error
        elif not str(numeros).isdigit():
            error = "Ingrese solo numeros enteros"
            return error
        else:
            listnumeros = list(str(numeros))
            for numero in listnumeros:
                acum = listnumeros.count(numero)
                if acum > 1:
                    error = "No puede repetir digitos"
                    return error
            return True
    except:
        error = "Hubo un error inesperado"
        return error


def valorarTirada(numeros, tirada):
    decimal = 0
    unidad = 0  # podria ser unidad, decimal = 0,0
    # convierto los int en lista para poder iterar
    listtirada = list(str(tirada))
    listnumeros = list(str(numeros))
    listborrar = []
    # itera las dos listas a la vez
    for digito, numero in zip(listtirada, listnumeros):
        if digito == numero:
            decimal += 1  # sumo solo si son iguales y en la misma posicion
            # guardo los elementos a borrar para no alterar el index de la lista
            listborrar.append(digito)
    for digito in listborrar:
        listtirada.remove(digito)
    for digito in listtirada:  # me fijo si en la lista quedo alguno en otro orden
        if digito in listnumeros:
            unidad += 1
            listnumeros.remove(digito)
    resultado = [decimal, unidad]
    return resultado
