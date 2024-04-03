from flask import Flask, send_file, request, abort, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

video_time = 0
usuarios = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    try:
        caminho_video = os.path.join(app.static_folder, 'video.mp4')
        if not os.path.exists(caminho_video):
            abort(404)
        return send_file(caminho_video, mimetype='video/mp4')
    except Exception as e:
        print(f'Erro ao servir o vídeo: {e}')
        abort(500)

@socketio.on('connect')
def handle_connect():
    print('Client connected: ' + request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected: ' + request.sid)
    if request.sid in usuarios:
        del usuarios[request.sid]

@socketio.on('time update')
def handle_time_update(data):
    global video_time
    if 'time' in data and isinstance(data['time'], (int, float)):
        video_time = data['time']
        emit('time update', {'time': video_time}, broadcast=True, include_self=False)
    else:
        print('Dados inválidos recebidos para atualização de tempo')

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('message', data, broadcast=True)

@socketio.on('username')
def handle_username(data):
    print('Received username:', data['username'])
    usuarios[request.sid] = data['username']
    emit('message', {'username': 'System', 'message': f'{data["username"]} entrou no chat'}, broadcast=True)
    emit('message', {'username': 'System', 'message': f'Usuários online: {", ".join(usuarios.values())}'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
