# import functools


from flask import Blueprint, render_template, session, redirect, url_for, g, flash
import datetime
from flask_socketio import emit
from app import mysql, mysocket
from resources import login_required,  authenticated_only, numeroOK, valorarTirada
from globals import make_sql_querry

main = Blueprint('no_auth_main', __name__)


@main.before_app_request
def if_logged():
    user_id = session.get('id')
    if user_id is None:
        g.user = None
    else:
        sql = "SELECT name FROM users WHERE id = %s"
        data = [user_id]
        g.user = make_sql_querry(mysql, sql, data, 'one')


@ main.route('/')
def index():
    return render_template('base.html')


@ main.route('/profile')
@ login_required
def profile():
    flash(str(g.user)[1:-2])  # mostrar el nombre del usuario logueado
    return render_template('profile.html')


@ main.route('/ranks')
@ login_required
def ranks():
    flash(str(g.user)[1:-2])
    partidas = (('mail', 'jugadas', 'ganadas', 'abandonadas'),
                ('mail', 'jugadas', 'ganadas', 'abandonadas'))
    return render_template('ranking.html', partidas=partidas)


@ main.route('/buscarsala')
@ login_required
def buscarSala():
    locked = False
    mail = session.get('mail')
    flash(str(g.user)[1:-2])
    sql = "SELECT sala, creador FROM salas WHERE abierta = True"
    salas = make_sql_querry(mysql, sql, None, 'all')
    for sala in salas:
        if sala[1] == mail:
            locked = True
    return render_template('buscarsala.html', salas=salas, locked=locked)


@ main.route('/uniendose/<sala>')
@ login_required
def uniendose(sala):
    flash(str(g.user)[1:-2])
    auth = False
    jugadores = ()
    jugando = False
    sql = "SELECT abierta FROM salas WHERE sala = (%s)"
    data = [sala]
    abierta = bool(make_sql_querry(mysql, sql, data, 'one'))
    # si la sala esta abierta pregunto si el jugador es el creador de la sala
    # cargo los jugadores en la misma
    if abierta:
        mail = session.get('mail')
        sql = f'SELECT creador FROM salas WHERE sala = (%s)'
        data = [sala]
        creador = make_sql_querry(mysql, sql, data, 'one')

        # si el usuario no es el creador no puede iniciar la partida
        if mail == creador[0]:
            auth = True
        # cargo lista de jugadores
        sql = "SELECT * FROM players WHERE sala = (%s)"
        data = [sala]
        jugadores = make_sql_querry(mysql, sql, data, 'all')
        # busco si esta el jugador en sala
        jugando = False
        for jugador in jugadores:
            # jugador =(index, mail, sala, numero, turno, turnoboolean)
            if jugador[1] == mail:
                jugando = True
            else:
                session['tmp_sala'] = jugador[2]
    else:
        # redirijo a los jugadores a la sala en juego
        # PROCESARRRRRRR
        pass
    toReturn = (auth, jugadores, jugando)
    return render_template('uniendose.html', datos=toReturn)


@ main.route('/lonumero')
@ login_required
def loNumero():
    flash(str(g.user)[1:-2])  # mostrar el nombre del usuario logueado
    mail = session.get('mail')
    sql = "select * from salas where creador = (%s)"
    data = [mail]
    sala = make_sql_querry(mysql, sql, data, 'one')
    sql = "select * from tiradas where room = (%s) and mail = (%s)"
    data = (sala, mail)
    tiradas = make_sql_querry(mysql, sql, data, 'all')
    if tiradas is None:
        return 'sala no encontrada'
    return render_template('lonumero.html', tiradas=tiradas)


@ main.route('/terms')
def terms():
    flash(str(g.user)[1:-2])
    return render_template('terms.html')


# ----------------------------------------------------------------------------------
# socket
# ----------------------------------------------------------------------------------

@ mysocket.on('login')
def on_login_user(data):
    emit('status_change', {'username': data}, broadcast=True)


@ mysocket.on('logout')
@ authenticated_only
def handleLogout():
    mail = session.get('mail')
    emit('status_change', {
         'username': f'{mail} ya no nos ama!! :( '}, broadcast=True)


@ mysocket.on('crear_sala')
@ authenticated_only
def setsala(sala, num):
    if numeroOK(num) == True:
        if len(sala) > 1 < 10:
            sql = "SELECT * FROM salas WHERE sala = (%s) "
            data = [sala]
            existe = make_sql_querry(mysql, sql, data, 'one')
            if existe is None:
                mail = session.get('mail')
                # inserto nueva sala
                sql = "INSERT INTO salas (sala, creador) values (%s,%s);"
                data = (sala, mail)
                make_sql_querry(mysql, sql, data)
                # inserto numero elegido por player  y asocio a sala
                sql = "INSERT INTO players (mail, sala, numero, turno, turnoboolean) values (%s,%s,%s,%s,%s);"
                data = (mail, sala, int(num), 1, True)
                make_sql_querry(mysql, sql, data)
                emit('redirect', {'url': url_for('no_auth_main.buscarSala')})

            else:
                error = 'La sala existe en otra instancia, cree otro codigo'
                emit('error', {'error': error})
                emit('redirect', {'url': url_for(
                    'no_auth_main.buscarSala')})  # no envia variables :(
    else:
        error = 'El numero ingresado no es valido'
        emit('error', {'error': error})
        emit('redirect', {'url': url_for(
            'no_auth_main.buscarSala')})


@ mysocket.on('set_number')
@ authenticated_only
# player:(index, mail, sala, numero, turno, turnoboolean)
def cargar_player(data, turno):

    if numeroOK(data) == True:
        mail = session.get('mail')
        sala = session.get('tmp_sala')
        sql = "INSERT INTO players (mail, sala, numero, turno, turnoboolean) values (%s,%s,%s,%s,%s);"
        vars = (mail, sala, data, int(turno)+1, False)
        make_sql_querry(mysql, sql, vars)
        emit('redirect', {'url': sala})
    else:
        error = 'El numero ingresado no es valido'
        emit('error', {'error': error})


@ mysocket.on('tirada')
@ authenticated_only
def handleTirada(data):
    if numeroOK(data) == True:
        mail = session.get('mail')
        adivinar = 4567  # desarrollar de donde obtenerlo
        resultado = float(valorarTirada(adivinar, data))
        room = "todo55"
        sql = "INSERT INTO tiradas (numero, resultado, room, mail) values (%s,%s,%s,%s);"
        values = (int(data), resultado, room, mail)
        make_sql_querry(mysql, sql, values)
        emit('redirect', {'url': url_for('no_auth_main.loNumero')})
    else:
        emit('error', {'error': 'Mala Tirada'})


@ mysocket.on('chat')
@ authenticated_only
def handleMessage(data):
    email = session.get('mail')
    now = datetime.datetime.now()
    if len(data) > 0:
        emit('receive_chat', {
            'texto': f'[{str(now)[:-7]}] {email}: {data}'}, broadcast=True)
