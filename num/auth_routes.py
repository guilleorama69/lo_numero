
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
# from app import mysql
from resources import on_login, exists_mail, create_user


auth = Blueprint('auth_routes', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        error = ""
        data = on_login()
        if data:
            flash(data[0])
            session.clear()
            session['name'] = data[0]
            session['id'] = data[2]
            session['mail'] = data[3]
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
        password = request.form.get('password')
        if len(password) < 8 or len(password) > 20:
            error = 'Compruebe su password'
            return render_template('signup.html', error=error)
        birthday = request.form.get('birthday')
        if len(birthday) == 0:
            error = 'Compruebe Fecha'
            return render_template('signup.html', error=error)
        gender = request.form.get('gender')
        if exists_mail(email):
            error = "El Usuario ya existe"
            return render_template('signup.html', error=error)
        else:
            create_user(email, name, lastname, password, birthday, gender)
    return redirect(url_for('auth_routes.login'))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('no_auth_main.index'))
