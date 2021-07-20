
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_socketio import emit
from app import mysocket
from resources import on_login, if_exists, create_user


auth = Blueprint('auth_routes', __name__)


@auth.route('/login')
def login():
    mail = session.get('mail')
    if mail:
        session.clear()
        return redirect(url_for('auth_routes.login'))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        error = ""
        data = on_login()
        # data =  name, pass, id, mail, nickname
        if data:
            flash(data[0])
            session.clear()
            session['name'] = data[0]
            session['id'] = data[2]
            session['mail'] = data[3]
            session['nick'] = data[4]
            nick = data[4]
            mysocket.emit('status_change', {'username': nick}, broadcast=True)
            return redirect(url_for('no_auth_main.buscarSala'))
        else:
            error = "Usuario o Password Incorrectos"
            return render_template('login.html', error=error)


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    error = ""
    if request.method == 'POST':
        name = request.form.get('firstname')
        if len(name) < 1 or len(name) > 35:
            error = 'Compruebe su nombre'
            return render_template('signup.html', error=error)
        lastname = request.form.get('lastname')
        if len(lastname) < 1 or len(lastname) > 35:
            error = 'Compruebe su Apellido'
            return render_template('signup.html', error=error)
        email = request.form.get('email')
        if len(email) < 1 or len(email) > 35:
            error = 'Compruebe su email'
            return render_template('signup.html', error=error)
        nickname = request.form.get('nickname')
        if len(nickname) < 1 or len(nickname) > 35:
            error = 'Compruebe su Nickname'
            return render_template('signup.html', error=error)
        password = request.form.get('password')
        if len(password) < 8 or len(password) > 20:
            error = 'Compruebe su password'
            return render_template('signup.html', error=error)
        birthday = request.form.get('birthday')
        if len(birthday) == 0:
            error = 'Compruebe Fecha'
            return render_template('signup.html', error=error)
        gender = request.form.get('gender')
        if if_exists('mail', 'users', email):
            error = "El Usuario ya existe"
            return render_template('signup.html', error=error)
        elif if_exists('nickname', 'users', nickname):
            error = "El Usuario ya existe"
            return render_template('signup.html', error=error)
        else:
            create_user(email, name, nickname, lastname,
                        password, birthday, gender)
    return redirect(url_for('auth_routes.login'))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('no_auth_main.index'))
