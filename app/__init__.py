from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    from .controllers.url_controller import url_bp
    from .controllers.chat_controller import chat_bp

    app.register_blueprint(url_bp)
    app.register_blueprint(chat_bp)
    
    return app
