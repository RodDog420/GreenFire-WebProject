/*
==========================================================================
CHAT.JS
Handles floating chat bubble open/close and message sending.
API calls go to /api/chat (Flask route — chat.py blueprint).
Model selection deferred to build time per project spec.
==========================================================================
*/

document.addEventListener('DOMContentLoaded', function () {
    const trigger = document.getElementById('chat-bubble-trigger');
    const chatWindow = document.getElementById('chat-window');
    const closeBtn = document.getElementById('chat-close');
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send');
    const messages = document.getElementById('chat-messages');

    if (!trigger || !chatWindow) return;

    // --- Toggle open/close ---

    trigger.addEventListener('click', function () {
        const isOpen = chatWindow.classList.toggle('is-open');
        trigger.setAttribute('aria-expanded', isOpen.toString());
        if (isOpen && input) input.focus();
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            chatWindow.classList.remove('is-open');
            trigger.setAttribute('aria-expanded', 'false');
            trigger.focus();
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && chatWindow.classList.contains('is-open')) {
            chatWindow.classList.remove('is-open');
            trigger.setAttribute('aria-expanded', 'false');
            trigger.focus();
        }
    });

    // --- Send message ---

    function sendMessage() {
        if (!input) return;
        const text = input.value.trim();
        if (!text) return;

        // Render user message
        appendMessage(text, 'user');
        input.value = '';
        input.style.height = 'auto';

        // Send to Flask /api/chat
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            appendMessage(data.reply || 'Something went wrong — please try again.', 'agent');
        })
        .catch(function () {
            appendMessage('Having trouble connecting right now. Try again in a moment.', 'agent');
        });
    }

    function appendMessage(text, sender) {
        if (!messages) return;
        const div = document.createElement('div');
        div.className = 'chat-message chat-message-' + sender;
        div.textContent = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    if (input) {
        // Send on Enter (but not Shift+Enter)
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-resize textarea
        input.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }
});
