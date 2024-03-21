from flask import Flask, send_file, request, abort
from flask_socketio import SocketIO, emit
import os
import time

# Criando a aplicação Flask e definindo a pasta de vídeos estáticos
app = Flask(__name__, static_folder='videos')
socketio = SocketIO(app, cors_allowed_origins="*")

# Variável global para armazenar a posição atual do vídeo
video_time = 0

# Definindo a rota para acessar o vídeo
@app.route('/video')
def video():
    try:
        # Definindo o caminho para o vídeo
        caminho_video = 'videos/video.mp4'
        # Verifica se o arquivo de vídeo existe
        if not os.path.exists(caminho_video):
            abort(404)  # Arquivo não encontrado
        # Enviando arquivo de vídeo completo
        return send_file(caminho_video, mimetype='video/mp4')
    except Exception as e:
        print(f'Erro ao servir o vídeo: {e}')
        abort(500)  # Erro interno do servidor

@socketio.on('connect')
def handle_connect():
    print('Client connected: ' + request.sid)
    # Emitir o evento 'play' para o novo cliente com a posição atual do vídeo
    emit('play', {'time': video_time})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected: ' + request.sid)

@socketio.on('time update')
def handle_time_update(data):
    global video_time
    # Validação dos dados recebidos
    if 'time' in data and isinstance(data['time'], (int, float)):
        video_time = data['time']
    else:
        print('Dados inválidos recebidos para atualização de tempo')
        
@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('message', data, broadcast=True)  # Emitir a mensagem recebida para todos os clientes

# Evento para enviar o nome do usuário quando entrar
@socketio.on('username')
def handle_username(data):
    print('Received username:', data['username'])
    emit('message', {'username': 'System','message': f'{data["username"]} - entrou no chat'}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, port=3000)
