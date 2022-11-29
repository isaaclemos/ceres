from os import path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    app.config['SECRET_KEY'] = 'e0cb7ed7e8de8d8ed8c46ea93dbfab3c764f62128f71141c161789896c3d747f'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/banco.db'
    db.init_app(app)


def create_database(app):
    if not path.exists(f'{app.root_path}/banco.db'):
        with app.app_context():
            db.create_all()
            create_admin()
        print('Created Database!')


def create_admin():
    from app.models import User

    user_name = 'admin'
    email = 'admin@admin'

    if not User.query.filter_by(email=email).first():
        user = User(user_name=user_name, email=email,
                    password="admin", is_admin=True)
        db.session.add(user)
        db.session.commit()
