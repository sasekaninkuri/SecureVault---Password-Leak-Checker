from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from flask_session import Session

mongo = PyMongo()
session = Session()

def create_app():
    app.config.from_object(Config)
    mongo.init_app(app)
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    from .controllers.url_controller import url_bp
    from .controllers.chat_controller import chat_bp

    app.register_blueprint(url_bp)
    app.register_blueprint(chat_bp)
    
    return app
