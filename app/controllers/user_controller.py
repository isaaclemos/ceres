import plotly.express as px
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.ext.database import db
from app.models import User


class UserController:

    before_request = ['check_is_authenticated']

    @login_required
    def check_is_authenticated(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.index'))

    def index(self):
        return render_template('home.html', title='Pagina inicial')

    def user_show(self):
        users = User.query.all()
        return render_template('admin/user.html', title='Usuarios', users=users)

    def create(self):
        self.create_user()
        return redirect(url_for('admin.user_show'))
    
    def edit(self):
        user = User.query.get(id)
        
        if user:
            return render_template('admin/form_user.html', user=user)        
        else:            
            return redirect(url_for('admin.user_show'))      

    def update(self, id):
        self.create_user(user_id=id, update=True)
        return redirect(url_for('admin.user_show'))

    def delete(self, id):
        user = User.query.get(id)

        if user:
            if user.id == current_user.id:
                flash('Não é possivel remover o usuario atual.', category='error')
            else:
                db.session.delete(user)
                db.session.commit()

                if User.query.get(id):
                    flash('Erro ao remover usuario.', category='error')
                else:
                    flash('Usuario removido com sucesso.', category='success')
        else:
            flash('Usuario não encontrado.', category='error')

        return redirect(url_for('admin.user_show'))

    def profile(self):
        return render_template('user/profile.html', title='Perfil')

    def profile_update(self):

        self.create_user(user_id=current_user.id, update=True, profile=True)
        return redirect(url_for('user.index'))

    def create_user(self, user_id=None, update=False, profile=False):

        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        is_admin = request.form.get('is_admin') == 'on'

        if update:
            user = User.query.get(user_id)
        else:
            user = User.query.filter_by(email=email).first()

        if request.method == 'POST':
            if user and not update:
                flash('Endereço de email existente.', category='error')
            elif len(email) < 4:
                flash('Endereço de email deve possuir no minimo 3 caracteres.',
                      category='error')
            elif len(user_name) < 4:
                flash('O nome deve possuir no minimo 3 caracteres', category='error')
            elif password1 != password2:
                flash('As senhas são diferentes.', category='error')
            elif len(password1) < 6:
                flash('A senha deve possuir no minimo 6 caracteres.',
                      category='error')
            else:

                if not update:
                    user = User(email=email, user_name=user_name,
                                password=password1, is_admin=is_admin)
                    db.session.add(user)
                    flash('Usuario cadastrado!', category='success')
                else:
                    user.user_name = user_name
                    user.email = email
                    user.set_password(password1)
                    if profile == False:
                        user.is_admin = is_admin
                    flash('Dados atualizados!', category='success')
                db.session.commit()

        return user
