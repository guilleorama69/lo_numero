from app import mysocket
from flask import Blueprint


class UserLogged:
    def __init__(self, name, id, state=True, game_id="", turn=False):
        name = self.__name
        id = self.__id

    @property
    def state(self):
        return UserLogged.__state

    @state.setter
    def set_state(self, state):
        UserLogged.__state = state
        return

    @property
    def game_id(self):
        return UserLogged.__game_id

    @game_id.setter
    def set_game_id(self, game_id):
        UserLogged.__game_id = game_id
        return

    @property
    def turn(self):
        return UserLogged.__turn

    @turn.setter
    def set_turn(self, turn):
        UserLogged.__turn = turn
        return


class IOBlueprint(Blueprint):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.namespace = self.url_prefix or '/'
        self._socketio_handlers = []
        self.socketio = None
        self.record_once(self.init_socketio)

    def init_socketio(self, state):
        self.socketio: mysocket.Client = state.app.extensions['mysocket']
        for f in self._socketio_handlers:
            f(self.socketio)

        return self.socketio

    def on(self, key):
        """ A decorator to add a handler to a blueprint. """

        def wrapper(f):
            def wrap(sio):
                @sio.on(key, namespace=self.namespace)
                def wrapped(*args, **kwargs):
                    return f(*args, **kwargs)

                return sio

            self._socketio_handlers.append(wrap)

        return wrapper

    def emit(self, *args, **kwargs):
        self.socketio.emit(*args, **kwargs)
