# import functools


from re import T
from flask import Blueprint, render_template, session, redirect, url_for, g, flash
#from werkzeug.wrappers import request
from flask_socketio import emit
from app import mysql, mysocket
from resources import login_required, make_sql_querry, authenticated_only, numeroOK, valorarTirada


main = Blueprint('no_auth_main', __name__)


@main.before_app_request
def if_logged():
    user_id = session.get('id')
    if user_id is None:
        g.user = None
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name FROM users WHERE id = %s', [user_id])
        g.user = cursor.fetchone()


@main.route('/')
def index():
    return render_template('base.html')


@main.route('/profile')
@login_required
def profile():
    flash(str(g.user)[1:-2])  # mostrar el nombre del usuario logueado
    return render_template('profile.html')


@main.route('/buscarsala')
@login_required
def buscarSala():
    locked = False
    mail = session.get('mail')
    flash(str(g.user)[1:-2])
    sql = 'SELECT sala, creador FROM salas WHERE abierta = True'
    salas = make_sql_querry(sql)
    for sala in salas:
        if sala[1] == mail:
            locked = True
    return render_template('buscarsala.html', salas=salas, locked=locked)


@mysocket.on('crear_sala')
@authenticated_only
def setsala(sala):
    if len(sala) > 1 < 10:
        sql = f'SELECT * FROM salas WHERE sala = \"{sala}\";'
        existe = str(make_sql_querry(sql))[1:-1]
        if len(existe) > 1:
            print('------------------------')
            print(existe)
            print('------------------------')
            error = 'La sala existe en otra instancia, cree otro codigo'
            render_template('buscarsala.html', error=error)
        else:
            mail = session.get('mail')
            sql = f'INSERT INTO salas (sala, creador) values (\"{sala}\", \"{mail}\");'
            print('------------------------')
            print(sql)
            print('------------------------')
            make_sql_querry(sql)
            render_template('buscarsala.html')


@main.route('/lonumero')
@login_required
def loNumero():
    flash(str(g.user)[1:-2])  # mostrar el nombre del usuario logueado
    mail = session.get('mail')
    sql = f'select * from salas where creador =  \"{mail}\"'
    sala = make_sql_querry(sql)
    sql = f'select * from tiradas where room = \"{sala}\" and mail = \"{mail}\"'
    tiradas = make_sql_querry(sql)
    if tiradas is None:
        return 'sala no encontrada'
    return render_template('lonumero.html', tiradas=tiradas)


@main.route('/terms')
def terms():
    return render_template('terms.html')


@mysocket.on('login')
def on_login_user(data):
    emit('status_change', {'username': data,
         'status': 'online'}, broadcast=True)


@mysocket.on('message')
@authenticated_only
def handleMessage(data):
    print(data)
    # emit(data, broadcast=True)


@mysocket.on('logout')
@authenticated_only
def handleLogout(data):
    print(data)


@mysocket.on('tirada')
@authenticated_only
def handleTirada(data):
    if numeroOK(data) == True:
        mail = session.get('mail')
        resultado = float(valorarTirada(4567, data))
        sql = f'insert into tiradas (numero, resultado, room, mail) values ({data},{resultado}, "az3456", \"{mail}\");'
        make_sql_querry(sql)
        redirect(url_for('no_auth_main.loNumero'))
    else:
        flash('Mala tirada', 'error')
