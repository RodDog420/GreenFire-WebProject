/*
==========================================================================
CHAT.JS — Penny AI assistant
Handles chat bubble open/close and message send/receive.
Conversation history is maintained in memory and sent with each request
so Penny has context of the full session.
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

    // Conversation history — grows with each completed round-trip
    var conversationHistory = [];

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

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && chatWindow.classList.contains('is-open')) {
            chatWindow.classList.remove('is-open');
            trigger.setAttribute('aria-expanded', 'false');
            trigger.focus();
        }
    });

    // --- Typing indicator ---

    function showTyping() {
        if (!messages) return null;
        const div = document.createElement('div');
        div.className = 'chat-message chat-message-agent chat-message-typing';
        div.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        return div;
    }

    function removeTyping(el) {
        if (el && el.parentNode) el.parentNode.removeChild(el);
    }

    // --- Send message ---

    function sendMessage() {
        if (!input) return;
        const text = input.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        input.value = '';
        input.style.height = 'auto';

        const typingEl = showTyping();

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                history: conversationHistory
            })
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            removeTyping(typingEl);
            const reply = data.reply || 'Something went wrong — please try again.';
            appendMessage(reply, 'agent');
            // Push completed round-trip to history for next message
            conversationHistory.push({ role: 'user', content: text });
            conversationHistory.push({ role: 'assistant', content: reply });
        })
        .catch(function () {
            removeTyping(typingEl);
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
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        input.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }
});
