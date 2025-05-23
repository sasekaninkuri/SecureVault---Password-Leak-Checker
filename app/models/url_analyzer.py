from urllib.parse import urlparse
import ipaddress
import tldextract
import whois
from datetime import datetime

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
            "whois": {},
            "ssl": {}
        }

        score = 0
        flags = []
        domain_info = {}
        ssl_info = {}

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
            domain = f"{extracted.domain}.{extracted.suffix}".lower()

            # HTTPS Check
            if parsed.scheme != 'https':
                result["https_check"] = "Insecure (HTTP)"
                flags.append("Uses HTTP instead of HTTPS")
                score += 1
            else:
                result["https_check"] = "Secure (HTTPS)"

            # Check if IP address used
            try:
                ipaddress.ip_address(parsed.hostname)
                flags.append("Uses IP address instead of domain")
                score += 2
                result["domain_analysis"] = "Uses IP address instead of domain"
            except ValueError:
                result["domain_analysis"] = "Domain format is valid"

            # Suspicious TLD Check
            suspicious_tlds = {'.ru', '.cn', '.tk', '.ml', '.ga'}
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                flags.append(f"Suspicious TLD: {domain}")
                score += 2
                result["domain_analysis"] += " + Suspicious TLD"

            # WHOIS Analysis
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
                    "domain_name": str(whois_data.domain_name),
                    "registrar": str(whois_data.registrar),
                    "creation_date": str(creation_date),
                    "expiration_date": str(whois_data.expiration_date)
                }
            except Exception:
                flags.append("WHOIS lookup failed")
                domain_info = {
                    "domain_name": "N/A",
                    "registrar": "N/A",
                    "creation_date": "N/A",
                    "expiration_date": "N/A"
                }

            # Redirect check — fake for now
            result["redirect_check"] = "No redirect detected (stub)"

            # Dummy SSL info
            ssl_info = {
                "issuer": [["CN", "Let's Encrypt"]],
                "notAfter": "2025-12-31"
            }

            # Phishing risk summary
            result["phishing_risk"] = "High" if score >= 4 else "Low"
            result["verdict"] = "Suspicious" if score >= 4 else "Likely Safe"
            result["score"] = score
            result["flags"] = flags
            result["whois"] = domain_info
            result["ssl"] = ssl_info

        except Exception as e:
            return {"error": str(e)}

        return result
        
