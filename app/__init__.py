from flask import Flask
from flask_login import LoginManager
from app.database import db, create_database
from app.models import *
from app.controllers import *

controllers= [
    auth_bp,
    home_bp,
    admin_bp,
    user_bp
]

DB_NAME = 'banco.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/{ DB_NAME}'
    db.init_app(app)

    for c in controllers:
        app.register_blueprint(c)
    
    create_database(app, DB_NAME)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor faça o login!'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

