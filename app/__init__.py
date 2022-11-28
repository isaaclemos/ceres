from flask import Flask
from app.ext import login_manager, database
from app.controllers import *
from app.resources import *

controllers= [
    auth_bp,
    admin_bp,
    user_bp,
    service_bp
]


def create_app():
    app = Flask(__name__)

    for c in controllers:
        app.register_blueprint(c)

    database.init_app(app)
    login_manager.init_app(app)
    
    database.create_database(app)


    return app

