from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.ext.database import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')        
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):                
                login_user(user, remember=True)
                return redirect(url_for('user.index'))
        else:
            flash('Email ou senha invalida.', category='error')

    return render_template("auth/login.html", user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



