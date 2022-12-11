from flask import Flask
from mvc_flask import FlaskMVC

from app.ext import database, login_manager

def create_app():
    
    app = Flask(__name__)
    
    FlaskMVC(app)

    database.init_app(app)
    login_manager.init_app(app)

    database.create_database(app)

    return app
