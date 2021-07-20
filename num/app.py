
from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
from globals import get_env_config

db = get_env_config('DBNAME', 'env.cfg')
host = get_env_config('DBHOST', 'env.cfg')
secretkey = get_env_config('SECRETKEY', 'env.cfg')
dbuser = get_env_config('DBUSER', 'env.cfg')
password = get_env_config('DBPASS', 'env.cfg')
debugOn = get_env_config('DEBUG', 'env.cfg')
#print(f'db:{db}, user:{dbuser}, pass:{password}, host:{host}, key:{secretkey}, debug:{debugOn}')
mysql = MySQL()
mysocket = SocketIO()
# ----------------
# debuggingggggggg
# cursor= mysql.connection.cursor()
# cursor.


def create_app():
    app = Flask(__name__)
    app.debug = debugOn
    app.config['SECRET_KEY'] = secretkey

    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = dbuser
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = db
    mysql = MySQL(app)

    # blueprint
    from auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # # blueprint
    from no_auth_main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    mysocket.init_app(app, logger=True, engineio_logger=True)

    return app


# if __name__ == '__main__':
#     app = create_app()
#     mysocket = SocketIO(app, logger=True, engineio_logger=True)
#     mysocket.run(app, port=5000, host='0.0.0.0')
