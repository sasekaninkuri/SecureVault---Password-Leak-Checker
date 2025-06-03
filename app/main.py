from app import create_app
from flask_session import Session

app = create_app()

app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Enforce same-site cookies
app.secret_key = 'your_secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

if __name__ == "__main__":
    app.run(debug=True)
