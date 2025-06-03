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



  const backToTop = document.getElementById("backToTop");

  window.onscroll = function () {
    backToTop.style.display = (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100)
      ? "block"
      : "none";
  };
  
  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }




  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  window.onscroll = function () {
    const btn = document.getElementById("backToTop");
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
      btn.style.display = "block";
    } else {
      btn.style.display = "none";
    }
  };

  function exportReport() {
    window.print();
  }

  function saveToHistory(url) {
    if (!url.trim()) return; // Prevent empty URLs
    let history = JSON.parse(localStorage.getItem("urlHistory")) || [];
    history.push(url);
    localStorage.setItem("urlHistory", JSON.stringify(history));
    displayHistory();
  }

  function displayHistory() {
    const history = JSON.parse(localStorage.getItem("urlHistory")) || [];
    const historyList = document.getElementById("historyList");
    historyList.innerHTML = ""; // Clear existing list items
    if (history.length === 0) {
      historyList.innerHTML = "<li>No history yet.</li>"; // Display a message if empty
    } else {
      history.forEach(url => {
        const li = document.createElement("li");
        li.textContent = url;
        historyList.appendChild(li);
      });
    }
  }

  // --- New Function: clearHistory() ---
  function clearHistory() {
    if (confirm("Are you sure you want to clear all history?")) {
      localStorage.removeItem("urlHistory"); // Remove the history from localStorage
      displayHistory(); // Update the displayed history (which will now be empty)
    }
  }
  // ------------------------------------

  let riskChartInstance = null;
  function updateRiskChart(score) {
    const ctx = document.getElementById('riskChart').getContext('2d');
    if (riskChartInstance) {
      riskChartInstance.destroy();
    }
    riskChartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Risk', 'Safe'],
        datasets: [{
          data: [score, 100 - score],
          backgroundColor: ['#f87171', '#34d399'],
        }]
      },
      options: { responsive: true, cutout: '80%' }
    });
  }

  async function analyzeURL() {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) {
      alert('Please enter a URL to analyze.');
      return;
    }

    saveToHistory(url);

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }

      const data = await response.json();

      document.getElementById('httpsStatus').innerText = data.https_check || "Error";
      document.getElementById('domainAnalysis').innerText = data.domain_analysis || "Error";
      document.getElementById('redirectInfo').innerText = data.redirect_check || "Error";
      document.getElementById('phishingRisk').innerText = data.phishing_risk || "Error";

      document.getElementById('result').innerHTML = `
        <strong>Verdict:</strong> ${data.verdict || 'N/A'}<br/>
        <strong>Notes:</strong> ${data.notes || 'None'}<br/>
        <strong>Score:</strong> ${data.score ?? 'N/A'}<br/><br/>

        <strong>WHOIS Info:</strong><br/>
        Domain: ${data.whois_info?.domain || 'N/A'}<br/>
        Registrar: ${data.whois_info?.registrar || 'N/A'}<br/>
        Created: ${data.whois_info?.created || 'N/A'}<br/>
        Expires: ${data.whois_info?.expires || 'N/A'}<br/><br/>

        <strong>SSL Certificate:</strong><br/>
        Issuer: ${data.ssl_certificate?.issuer || 'N/A'}<br/>
        Expires: ${data.ssl_certificate?.expires || 'N/A'}<br/><br/>

        ${data.suggestions ? '<strong>Suggestions:</strong> ' + data.suggestions.join(', ') : ''}
      `;

      updateRiskChart(data.score ?? 50);

    } catch (error) {
      alert('Error analyzing URL. Please try again later.');
      console.error(error);
    }
  }

  // Initial display of history when the page loads
  displayHistory();
