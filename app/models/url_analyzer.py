from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import ipaddress
import tldextract
import whois
from datetime import datetime

app = Flask(__name__)

class URLAnalyzer:
    def analyze_url(self, url):
        result = {
            "https_check": "",
            "domain_analysis": "",
            "redirect_check": "",
            "phishing_risk": "",
            "verdict": "",
            "score": 0,
            "flags": [],
            "whois_info": {},
            "ssl_certificate": {},
            "notes": "",
            "suggestions": []
        }

        score = 0
        flags = []
        domain_info = {}
        ssl_info = {}

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            parsed = urlparse(url)
            if not parsed.hostname:
                return {"error": "Invalid URL"}

            extracted = tldextract.extract(url)
            domain = f"{extracted.domain}.{extracted.suffix}".lower()

            # HTTPS Check
            if parsed.scheme != 'https':
                result["https_check"] = "Insecure (HTTP)"
                flags.append("Uses HTTP instead of HTTPS")
                score += 1
            else:
                result["https_check"] = "Secure (HTTPS)"

            # IP Address Check
            try:
                ipaddress.ip_address(parsed.hostname)
                flags.append("Uses IP address instead of domain")
                result["domain_analysis"] = "Uses IP address"
                score += 2
            except ValueError:
                result["domain_analysis"] = "Domain format is valid"

            # Suspicious TLD Check
            suspicious_tlds = {'.ru', '.cn', '.tk', '.ml', '.ga'}
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                flags.append(f"Suspicious TLD: {domain}")
                score += 2
                result["domain_analysis"] += " + Suspicious TLD"

            # WHOIS Lookup
            try:
                whois_data = whois.whois(domain)
                creation_date = whois_data.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]

                if creation_date and (datetime.now() - creation_date).days < 30:
                    flags.append("Newly registered domain")
                    score += 2
                    result["domain_analysis"] += " + Newly registered domain"

                domain_info = {
                    "domain": str(whois_data.domain_name) if whois_data.domain_name else "N/A",
                    "registrar": str(whois_data.registrar) if whois_data.registrar else "N/A",
                    "created": str(creation_date) if creation_date else "N/A",
                    "expires": str(whois_data.expiration_date) if whois_data.expiration_date else "N/A"
                }
            except Exception:
                flags.append("WHOIS lookup failed")
                domain_info = {
                    "domain": "N/A",
                    "registrar": "N/A",
                    "created": "N/A",
                    "expires": "N/A"
                }

            # Redirect check (stubbed)
            result["redirect_check"] = "No redirect detected (stub)"

            # Dummy SSL Certificate Info
            ssl_info = {
                "issuer": "Let's Encrypt",
                "expires": "2025-12-31"
            }

            # Verdict & Risk Score
            result["phishing_risk"] = "High" if score >= 4 else "Low"
            result["verdict"] = "Suspicious" if score >= 4 else "Likely Safe"
            result["notes"] = "Multiple red flags were found during analysis." if score >= 4 else "No malicious indicators found."
            result["suggestions"] = ["Avoid visiting", "Report to IT team"] if score >= 4 else ["Enable DNSSEC", "Monitor SSL renewal"]
            result["score"] = score
            result["flags"] = flags
            result["whois_info"] = domain_info
            result["ssl_certificate"] = ssl_info

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

        return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url', '')
    analyzer = URLAnalyzer()
    result = analyzer.analyze_url(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)




        
