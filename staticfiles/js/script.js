// messaging/static/js/script.js

// Scroll to bottom of message list on load
document.addEventListener("DOMContentLoaded", function() {
    var messageList = document.querySelector('.message-list');
    messageList.scrollTop = messageList.scrollHeight;
});

// Scroll to bottom of message list after sending a message
document.getElementById('message-form').addEventListener('submit', function() {
    var messageList = document.querySelector('.message-list');
    messageList.scrollTop = messageList.scrollHeight;
});
