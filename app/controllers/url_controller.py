from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models.url_analyzer import URLAnalyzer

url_bp = Blueprint('url_bp', __name__)
analyzer = URLAnalyzer()

def process_report(url, details):
    """
    Process the report submitted by the user.
    This could be logging, saving to a database, or alerting.
    """
    with open('url_analysis.log', 'a') as log_file:
        log_file.write(f"[REPORT] URL: {url} | Details: {details}\n")
    print(f"Report processed: URL={url}, Details={details}")

@url_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@url_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@url_bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@url_bp.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        url = request.form['url']
        details = request.form['details']
        process_report(url, details)  # Process the report
        flash('Report submitted successfully!', 'success')
        return redirect(url_for('url_bp.report'))  # Redirect to the report page

    return render_template('report.html')

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
            "score": result.get("score", 0),  # Default to 0 if missing
            "suggestions": result.get("suggestions", [])  # Ensure it's a list
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
