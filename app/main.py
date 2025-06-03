import os
from app import create_app
from flask_session import Session

app = create_app()

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Load secret key and session type from environment variables
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE', 'filesystem')

Session(app)

if __name__ == "__main__":
    app.run(debug=True)
