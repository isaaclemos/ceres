from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import User
from app.database import db

user_bp = Blueprint('user', __name__,url_prefix='/user')

@user_bp.before_request
@login_required
def check_admin():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@user_bp.route('/index', methods=['GET'])
def index():
    return render_template('home.html')

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():

    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        if user and user.id != current_user.id:
            flash('Endereço de email existente.', category='error')
        elif len(email) < 4:
            flash('Endereço de email deve possuir no minimo 3 caracteres.',
                  category='error')
        elif len(user_name) < 4:
            flash('O nome deve possuir no minimo 3 caracteres', category='error')
        elif password1 != password2:
            flash('As senhas são diferentes.', category='error')
        elif len(password1) < 6:
            flash('A senha deve possuir no minimo 6 caracteres.', category='error')
        else:
            current_user.user_name = user_name
            current_user.email = email
            current_user.set_password(password1)
            flash('Dados atualizados!', category='success')
            db.session.commit()
            return redirect(url_for('user.profile'))

    return render_template('user/profile.html', title='Perfil')

@user_bp.route('/stations', methods=['GET'])
def stations():
    stations = current_user.stations
    return render_template('user/station.html', title='Estações' ,stations=stations)

