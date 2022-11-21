from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
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


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        is_admin = request.form['is_admin'] in 'on'

        user = User.query.filter_by(email=email).first()
        if user:
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
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(
                password1, method='sha256'), is_admin=is_admin)
            db.session.add(new_user)                           
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Usuario cadastrado!', category='success')
            return redirect(url_for('home.index'))

    return render_template("auth/form.html", title='Novo Usuario')
