from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from app.models.user import User
from app.database import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')        
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):                
                login_user(user, remember=True)
                return redirect(url_for('home.index'))
            else:
                flash('Senha incorreta, por favor tente novamente.', category='error')
        else:
            flash('Email não existe.', category='error')

    return render_template("auth/login.html", user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



