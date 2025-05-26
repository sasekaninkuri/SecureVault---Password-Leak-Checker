from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory store for URL history
url_history = []

@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.json
    url = data.get('url')
    if url and url not in url_history:
        url_history.append(url)
    return jsonify({"status": "success", "history": url_history})

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify({"history": url_history})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    url_history.clear()
    return jsonify({"status": "cleared"})
