var socket = io.connect('http://10.50.198.131:3000');  // Trocar pelo ip que o servidor está
var video = document.getElementById('video');
var chat = document.getElementById('chat');
var messageForm = document.getElementById('message-form');
var messageInput = document.getElementById('message-input');
var usernameForm = document.getElementById('username-form');
var usernameInput = document.getElementById('username-input');
var isSeeking = false;
var lastSentTime = 0;

socket.on('play', function(data) {
    video.currentTime = data.time;
    video.play(); // Adicionado o play automático
});

socket.on('time update', function(data) {
    video.currentTime = data.time;
});

socket.on('message', function(data) {
    var p = document.createElement('p');
    if (data.username === 'System') {
        p.innerText = data.message;
    } else {
        p.innerText = `${data.username}: ${data.message}`;
    }
    chat.appendChild(p);
    chat.scrollTop = chat.scrollHeight;
});

usernameForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var username = usernameInput.value;
    socket.emit('username', {'username': username});
    showVideoAndChat();
});

function showVideoAndChat() {
    usernameForm.style.display = 'none';
    document.body.classList.add('nome-digitado');
    video.style.display = 'block';
    chat.style.display = 'block';
    messageForm.style.display = 'flex';

    setInterval(function() {
        if (!isSeeking) {
            socket.emit('time update', { time: video.currentTime });
        }
    }, 15000);
}

messageForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var message = messageInput.value;
    var username = usernameInput.value;
    socket.emit('message', {'username': username, 'message': message});
    messageInput.value = '';
});
