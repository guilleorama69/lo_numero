
from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO


mysql = MySQL()


def create_app(debug=False):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mi_gran_clave_secreta'
    app.debug = debug

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'guille'
    app.config['MYSQL_PASSWORD'] = 'mango69'
    app.config['MYSQL_DB'] = 'mycrud'
    mysql = MySQL(app)

    # blueprint
    from auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # # blueprint
    from no_auth_main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # mysocket.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app(debug=True)
    mysocket = SocketIO(app, logger=True, engineio_logger=True)
    mysocket.run(app, port=5000, host='0.0.0.0')
