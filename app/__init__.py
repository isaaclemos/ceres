from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/{ DB_NAME}'
    db.init_app(app)
        
    from app.views.auth import auth
    from app.views.home import home
    from app.views.admin import admin
    from app.views.user import user
    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(admin)
    app.register_blueprint(user)    

    from .models.user import User
    from .models.station import Station
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor faça o login!'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app




def create_database(app):
    if not path.exists(f'{app.root_path}/{ DB_NAME}'):
        with app.app_context():
            db.create_all()
        print('Created Database!')