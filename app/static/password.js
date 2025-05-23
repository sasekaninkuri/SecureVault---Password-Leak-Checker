// File: app/static/main.js

async function analyzeURL() {
  const url = document.getElementById('urlInput').value;

  if (!url) {
    alert("Please enter a URL.");
    return;
  }

  // Basic Local Analysis
  let parser;
  try {
    parser = new URL(url);
  } catch (e) {
    alert("Invalid URL format.");
    return;
  }

  // HTTPS Check
  const isHttps = parser.protocol === "https:";
  document.getElementById("httpsStatus").innerText = isHttps ? "✅ Secure (HTTPS)" : "❌ Not Secure (HTTP)";

  // Domain Analysis
  const domain = parser.hostname;
  const suspiciousKeywords = ["login", "secure", "verify", "bank"];
  const containsSuspicious = suspiciousKeywords.some(keyword => domain.includes(keyword));
  document.getElementById("domainAnalysis").innerText = containsSuspicious ? "⚠️ Suspicious keywords in domain" : "✅ No red flags";

  // Redirection Check
  const hasRedirect = url.toLowerCase().includes("redirect");
  document.getElementById("redirectInfo").innerText = hasRedirect ? "⚠️ May redirect" : "✅ No obvious redirection";

  // Phishing Risk Check
  const phishingRisk = domain.includes("google.com.") || domain.split('.').length > 3;
  document.getElementById("phishingRisk").innerText = phishingRisk ? "⚠️ Possible phishing pattern" : "✅ Low risk";

  // Backend Analysis via Flask
  const response = await fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });

  const data = await response.json();
  const resultDiv = document.getElementById('result');

  if (data.error) {
    resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
    return;
  }

  resultDiv.innerHTML = `
    <h2 class="subtitle">Verdict: ${data.verdict || 'Unknown'}</h2>
    <ul class="flags">
      ${data.flags?.map(flag => `<li>${flag}</li>`).join("") || '<li>None</li>'}
    </ul>
    <p class="score">Score: ${data.score ?? 'N/A'}</p>

    <div class="section">
      <h3>WHOIS Info:</h3>
      <p><strong>Domain:</strong> ${data.whois?.domain_name || "N/A"}</p>
      <p><strong>Registrar:</strong> ${data.whois?.registrar || "N/A"}</p>
      <p><strong>Created:</strong> ${data.whois?.creation_date || "N/A"}</p>
      <p><strong>Expires:</strong> ${data.whois?.expiration_date || "N/A"}</p>
    </div>

    <div class="section">
      <h3>SSL Certificate:</h3>
      <p><strong>Issuer:</strong> ${data.ssl?.issuer?.[0]?.[1] || "N/A"}</p>
      <p><strong>Expires:</strong> ${data.ssl?.notAfter || "N/A"}</p>
    </div>
  `;
}

  