var socket = io.connect('http://localhost:3000');
var video = document.getElementById('video');
var chat = document.getElementById('chat');
var messageForm = document.getElementById('message-form');
var messageInput = document.getElementById('message-input');
var usernameForm = document.getElementById('username-form');
var usernameInput = document.getElementById('username-input');
var isSeeking = false;
var lastSentTime = 0;

video.ontimeupdate = function() {
    socket.emit('time update', {'time': video.currentTime})
};

socket.on('play', function(data) {
    video.currentTime = data.time;
    video.play();
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
}

messageForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var message = messageInput.value;
    var username = usernameInput.value;
    socket.emit('message', {'username': username, 'message': message});
    messageInput.value = '';
});