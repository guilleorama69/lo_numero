# The most flexible type of event uses custom event names. The message data for these events can be string, bytes, int, or JSON:

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
# Custom named events can also support multiple arguments:

# @socketio.on('my_event')
# def handle_my_custom_event(arg1, arg2, arg3):
#     print('received args: ' + arg1 + arg2 + arg3)

# from flask_socketio import join_room, leave_room, send, emit
# from flask import render_template
# #from app import mysocket
# #from models import IOBlueprint
# from resources import authenticated_only

# # bp = IOBlueprint('events', __name__)


# # @bp.on('echo')
# # @authenticated_only
# # def on_alive(data):
# #     print(data)
# #     emit('echo', data)  # context aware emit


# @mysocket.on('login')
# def on_login_user(data):
#     print(f'el msg recibido es:{data}')
#     #emit('status_change', {'username': username, 'status': 'online', 'id':id}, broadcast=True)


# @mysocket.on('message', namespace='/')
# @authenticated_only
# def handleMessage(data):
#     print(data)
#     emit(data, broadcast=True)
#     return render_template('login.html')
