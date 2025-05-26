async function analyzeURL() {
  const url = document.getElementById('urlInput').value;

  if (!url) {
    alert("Please enter a URL.");
    return;
  }

  // Basic URL validation
  try {
    new URL(url);
  } catch (e) {
    alert("Invalid URL format.");
    return;
  }

  saveToHistory(url);

  const response = await fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });

  const data = await response.json();

  // Update UI with backend results or fallback to error text
  document.getElementById('httpsStatus').innerText = data.https_check || "Error";
  document.getElementById('domainAnalysis').innerText = data.domain_analysis || "Error";
  document.getElementById('redirectInfo').innerText = data.redirect_check || "Error";
  document.getElementById('phishingRisk').innerText = data.phishing_risk || "Error";

  // Display extended info in the result div
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
}

function toggleMode() {
  document.body.classList.toggle("dark-mode");
}

function exportReport() {
  window.print();
}

function saveToHistory(url) {
  let history = JSON.parse(localStorage.getItem("urlHistory")) || [];
  history.push(url);
  localStorage.setItem("urlHistory", JSON.stringify(history));
  displayHistory();
}

function displayHistory() {
  const history = JSON.parse(localStorage.getItem("urlHistory")) || [];
  const historyList = document.getElementById("historyList");
  historyList.innerHTML = "";
  history.forEach(url => {
    const li = document.createElement("li");
    li.textContent = url;
    historyList.appendChild(li);
  });
}

function updateRiskChart(score) {
  const ctx = document.getElementById('riskChart').getContext('2d');
  new Chart(ctx, {
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

// Initialize history on page load
displayHistory();

function clearHistory() {
  localStorage.removeItem("urlHistory");  // Clear saved URLs
  displayHistory();                       // Refresh displayed list
}

async function fetchHistory() {
  const res = await fetch('/get_history');
  const data = await res.json();
  displayHistory(data.history);
}

function displayHistory(history) {
  const historyList = document.getElementById("historyList");
  historyList.innerHTML = "";
  history.forEach(url => {
    const li = document.createElement("li");
    li.textContent = url;
    historyList.appendChild(li);
  });
}

async function saveToHistory(url) {
  if (!url.trim()) return;
  const res = await fetch('/add_url', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ url })
  });
  const data = await res.json();
  displayHistory(data.history);
}

async function clearHistory() {
  const res = await fetch('/clear_history', { method: 'POST' });
  const data = await res.json();
  if (data.status === "cleared") {
    displayHistory([]);
  }
}

function navigateTo(event, path) {
  event.preventDefault();
  console.log(`Navigating to: ${path}`);
  setTimeout(() => {
    window.location.href = path;
  }, 100); // slight delay if needed
}





  