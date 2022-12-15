from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models.user import User


class AuthController:
    
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('user.index'))
        
        return render_template("auth/login.html")
        
    def login(self):        
        email = request.form.get('email')
        password = request.form.get('password')        
           
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):                
            login_user(user, remember=True)            
            return redirect(url_for('user.index'))
        else:
            flash('Email ou senha invalida.', category='error')
            return redirect(url_for('auth.index'))        
   
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('auth.index'))



