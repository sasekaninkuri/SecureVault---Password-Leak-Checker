function toggleChat() {
    const chat = document.getElementById('educational-chat');
    chat.style.display = chat.style.display === 'none' || chat.style.display === '' ? 'block' : 'none';
  }

  // New sendMessage function to interact with Flask backend
  async function sendMessage() {
    const userInputField = document.getElementById('user-input');
    const userMessage = userInputField.value.trim();
    const chatBox = document.getElementById('chat-box');

    if (!userMessage) {
      return; // Don't send empty messages
    }

    // Display user message immediately
    chatBox.innerHTML += `<div class="user-msg">${userMessage}</div>`;
    userInputField.value = ''; // Clear input field
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom

    // Add a temporary "typing" indicator or loading message
    const thinkingMessage = document.createElement('div');
    thinkingMessage.classList.add('bot-msg', 'thinking-msg');
    thinkingMessage.textContent = 'CyberSec Bot is thinking...';
    chatBox.appendChild(thinkingMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
      const response = await fetch('/ask_cybersec_bot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      // Remove the thinking message
      chatBox.removeChild(thinkingMessage);

      if (!response.ok) {
        // Handle HTTP errors (e.g., 500 server error)
        const errorData = await response.json();
        const errorMessage = errorData.response || 'An unknown error occurred.';
        chatBox.innerHTML += `<div class="bot-msg error-msg">Error: ${errorMessage}</div>`;
      } else {
        const data = await response.json();
        const botReply = data.response;
        chatBox.innerHTML += `<div class="bot-msg">${botReply}</div>`;
      }
    } catch (error) {
      // Handle network errors or other issues with the fetch request
      console.error('Error sending message to bot:', error);
      chatBox.removeChild(thinkingMessage); // Remove thinking message even on network error
      chatBox.innerHTML += `<div class="bot-msg error-msg">Sorry, I can't connect to the bot right now. Please try again later.</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom after bot reply/error
  }