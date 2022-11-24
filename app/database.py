from os import path

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def create_database(app, db_name):
    if not path.exists(f'{app.root_path}/{db_name}'):
        with app.app_context():
            db.create_all()
            db.session.commit()
        print('Created Database!')
