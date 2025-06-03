from urllib.parse import urlparse
import ipaddress
import tldextract
import whois
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='url_analysis.log', level=logging.INFO)

class URLAnalyzer:
    def analyze_url(self, url):
        result = {
            "https_check": "",
            "domain_analysis": "",
            "redirect_check": "No redirect detected (stub)",  # Default stub
            "phishing_risk": "",
            "verdict": "",
            "score": 0,
            "flags": [],
            "whois": {},
            "ssl": {
                "issuer": "Let's Encrypt",  # Dummy info
                "expires": "2025-12-31"     # Dummy date
            }
        }

        score = 0
        flags = []
        domain_info = {}

        # Ensure proper URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            parsed = urlparse(url)
            if not parsed.hostname:
                return {"error": "Invalid URL"}

            extracted = tldextract.extract(url)
            domain = f"{extracted.domain}.{extracted.suffix}".lower()

            # === HTTPS Check ===
            if parsed.scheme != 'https':
                result["https_check"] = "Insecure (HTTP)"
                flags.append("Uses HTTP instead of HTTPS")
                score += 1
            else:
                result["https_check"] = "Secure (HTTPS)"

            # === IP Address Check ===
            try:
                ipaddress.ip_address(parsed.hostname)
                result["domain_analysis"] = "Uses IP address"
                flags.append("Uses IP address instead of domain")
                score += 2
            except ValueError:
                result["domain_analysis"] = "Domain format is valid"

            # === Suspicious TLD Check ===
            suspicious_tlds = {'.ru', '.cn', '.tk', '.ml', '.ga'}
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                result["domain_analysis"] += " + Suspicious TLD"
                flags.append(f"Suspicious TLD: {domain}")
                score += 2

            # === WHOIS Check ===
            try:
                whois_data = whois.whois(domain)
                creation_date = whois_data.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]

                if creation_date and (datetime.now() - creation_date).days < 30:
                    result["domain_analysis"] += " + Newly registered domain"
                    flags.append("Newly registered domain")
                    score += 2

                domain_info = {
                    "domain_name": str(whois_data.domain_name) if whois_data.domain_name else "N/A",
                    "registrar": str(whois_data.registrar) if whois_data.registrar else "N/A",
                    "creation_date": str(creation_date) if creation_date else "N/A",
                    "expiration_date": str(whois_data.expiration_date) if whois_data.expiration_date else "N/A"
                }
            except Exception as e:
                flags.append("WHOIS lookup failed")
                logging.error(f"WHOIS lookup failed for {domain}: {str(e)}")
                domain_info = {
                    "domain_name": "N/A",
                    "registrar": "N/A",
                    "creation_date": "N/A",
                    "expiration_date": "N/A"
                }

            # === Risk & Verdict Calculation ===
            result["phishing_risk"] = "High" if score >= 4 else "Low"
            result["verdict"] = "Suspicious" if score >= 4 else "Likely Safe"
            result["score"] = score
            result["flags"] = flags
            result["whois"] = domain_info

        except Exception as e:
            logging.error(f"Analysis failed for {url}: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}

        return result

def process_report(url, details):
    logging.info(f"Processing report: URL: {url}, Details: {details}")
    # Add logic to save or analyze the report here

