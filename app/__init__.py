from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .controllers.url_controller import url_bp
    app.register_blueprint(url_bp)
    
    return app
