import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'messenger_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f"{username} joined the chat."}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    emit('receive_message', {'sender': data['sender'], 'message': data['message']}, room=room)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
