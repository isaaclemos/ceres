from flask import Flask
from flask_login import LoginManager
from app.database import db, create_database
from app.models import *
from app.controllers import *
from app.resources import *

controllers= [
    auth_bp,
    admin_bp,
    user_bp,
    service_bp
]

DB_NAME = 'banco.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'e0cb7ed7e8de8d8ed8c46ea93dbfab3c764f62128f71141c161789896c3d747f'
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

