document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message');
    const messagesDiv = document.getElementById('messages');
    const loader = document.getElementById('loader');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        addMessageToChat(userMessage, 'user-message');

        messageInput.value = '';
        loader.style.display = 'block';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            addMessageToChat(data.response, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
            loader.style.display = 'none';
        });
    });

    function addMessageToChat(message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        messageDiv.textContent = message;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
