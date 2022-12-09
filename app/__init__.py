from flask import Flask

from app.controllers import admin_bp, auth_bp, user_bp
from app.ext import database, login_manager
from app.resources import service_bp

controllers = [
    auth_bp,
    admin_bp,
    user_bp,
    service_bp
]

def create_app():
    app = Flask(__name__)
    
    for controller in controllers:
        app.register_blueprint(controller)

    database.init_app(app)
    login_manager.init_app(app)

    database.create_database(app)

    return app
