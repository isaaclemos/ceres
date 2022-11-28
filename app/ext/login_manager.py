from flask_login import LoginManager
from app.models import User


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor faça o login!'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def init_app(app):
    login_manager.init_app(app)