from flask import Blueprint, render_template, request, jsonify
from app.models.url_analyzer import URLAnalyzer

url_bp = Blueprint('url_bp', __name__)
analyzer = URLAnalyzer()

@url_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@url_bp.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Perform URL analysis
        result = analyzer.analyze_url(url)

        # Ensure all expected fields are in response
        response = {
            "https_check": result.get("https_check", "Unknown"),
            "domain_analysis": result.get("domain_analysis", "Unknown"),
            "redirect_check": result.get("redirect_check", "Unknown"),
            "phishing_risk": result.get("phishing_risk", "Unknown"),
            "score": result.get("score", 50),  # Defaults to 50 if missing
            "suggestions": result.get("suggestions", [])  # List of improvement tips
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

