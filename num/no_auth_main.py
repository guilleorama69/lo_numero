# import functools
from flask import Blueprint, render_template, session, redirect, url_for, g, flash
from app import mysql
from resources import login_required


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


@main.route('/lonumero')
@login_required
def loNumero():
    flash(str(g.user)[1:-2])  # mostrar el nombre del usuario logueado
    return render_template('lonumero.html')


@main.route('/terms')
def terms():
    return render_template('terms.html')
