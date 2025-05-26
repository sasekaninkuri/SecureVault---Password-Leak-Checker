 #app/controllers/chat_controller.py

import google.generativeai as genai
import os
from flask import jsonify, request, Blueprint

chat_bp = Blueprint('chat', __name__)

# --- Configure Google Generative AI with your API key ---
# It is HIGHLY recommended to use environment variables for API keys in production.
# For local development, you would set GEMINI_API_KEY in your terminal before running Flask.
#
# Example (Linux/macOS): export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
# Example (Windows cmd): set GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
# Example (Windows PowerShell): $env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
#
# If you must hardcode for testing, uncomment the line below and replace the placeholder,
# but remember to switch to environment variables for deployment.
# genai.configure(api_key="YOUR_ACTUAL_GEMINI_API_KEY_HERE") # Only use for local testing, REMOVE FOR PRODUCTION!

# Fetch API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Log a warning if the API key environment variable is not set
    print("WARNING: GEMINI_API_KEY environment variable not set. Chatbot may not function correctly.")
    # In a production environment, you might want to raise an exception or provide
    # a more robust fallback/error handling mechanism here.

# Configure the Generative AI client with the API key
genai.configure(api_key=api_key)

# Initialize the generative model with a supported model name
# Based on your ListModels output, 'models/gemini-1.5-flash-latest' is a good choice for chatbots.
# It's fast and cost-effective for conversational AI.
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# --- Conversation History Management ---
# This global list will store the chat history for a single user session.
# IMPORTANT: For a multi-user application, you would need a more robust
# session management system (e.g., Flask sessions, database) to store
# history per user. For this demo, a global list is sufficient.
chat_history = []
MAX_HISTORY_LENGTH = 10 # Keep the last 10 messages (5 user, 5 bot turns)

@chat_bp.route('/ask_cybersec_bot', methods=['POST'])
def ask_cybersec_bot():
    global chat_history # Declare intent to modify the global chat_history list

    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"response": "No message provided."}), 400

    try:
        # Add the current user's message to the conversation history
        chat_history.append({"role": "user", "parts": [{"text": user_message}]})

        # Truncate history to keep it within the defined limit
        if len(chat_history) > MAX_HISTORY_LENGTH:
            chat_history = chat_history[-MAX_HISTORY_LENGTH:]

        # Generate content using the entire conversation history as context
        # The Gemini model will use the previous turns to understand the current query.
        response = model.generate_content(chat_history)

        # Extract the text from the AI's response
        bot_reply = response.text

        # Add the bot's reply to the conversation history
        chat_history.append({"role": "model", "parts": [{"text": bot_reply}]})

        return jsonify({"response": bot_reply})

    except Exception as e:
        # Log the full error to the Flask terminal for detailed debugging
        print(f"DEBUG: Error calling Gemini API: {e}")

        # Prepare a user-friendly error message for the frontend
        error_message_for_frontend = str(e)
        if len(error_message_for_frontend) > 200:
            error_message_for_frontend = error_message_for_frontend[:200] + "..."

        # Clear history on error to prevent sending a corrupted state in subsequent attempts
        chat_history.clear()

        # Return an error response to the frontend
        return jsonify({"response": f"Sorry, I'm having trouble connecting to my knowledge base right now. (Backend Error: {error_message_for_frontend})"}), 500