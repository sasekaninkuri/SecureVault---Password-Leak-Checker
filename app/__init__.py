from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session
from config import Config

mongo = PyMongo()
session = Session()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')  # FIRST, create the app
    
    app.config.from_object(Config)  # THEN, load the config
    mongo.init_app(app)
    session.init_app(app)

    from .controllers.url_controller import url_bp
    from .controllers.chat_controller import chat_bp

    app.register_blueprint(url_bp)
    app.register_blueprint(chat_bp)

    return app
