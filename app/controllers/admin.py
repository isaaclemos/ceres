from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app.models import User, Station
from app.database import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def check_admin():
    if not current_user.is_admin:
        return abort(403)


@admin_bp.route('/user', methods=['GET', 'POST'])
def user():
    users = User.query.all()
    return render_template('admin/user.html', title='Usuarios', users=users)


@admin_bp.route('/user/insert', methods=['POST'])
def user_insert():
    create_user()
    return redirect(url_for('admin.user'))


@admin_bp.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def user_edit(id):
    user = create_user(user_id=id, update=True)

    if request.method == 'POST':
        return redirect(url_for('admin.user'))
    else:
        return render_template('admin/form_user.html', user=user, title='Atualizar usuario')


@admin_bp.route('/user/<int:id>/delete', methods=['GET'])
def user_delete(id):
    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()

        if User.query.get(id):
            flash('Erro ao remover usuario.', category='error')
        else:
            flash('Usuario removido com sucesso.', category='success')
    else:
        flash('Usuario não encontrado.', category='error')

    return redirect(url_for('admin.user'))


@admin_bp.route('/user/<int:id>/station', methods=['GET'])
def stations_by_user(id):
    stations = User.query.get(id).stations
    return render_template('admin/station.html', title='Estações', stations=stations)


@admin_bp.route('/station/user/<int:id>/insert', methods=['POST'])
def station_insert(id):
    return render_template('admin/form_station.html', title='Estação')


@admin_bp.route('/station/edit/<int:id>', methods=['GET', 'POST'])
def edit_station(id):
    
    station = Station.query.get(id)
    
    if request.method == 'POST':
        print(request.form.get('altitude'))
    

    return render_template('admin/form_station.html', title='Estação', station=station)


def create_user(user_id=None, update=False):

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
            flash('A senha deve possuir no minimo 6 caracteres.', category='error')
        else:
            password = generate_password_hash(password1, method='sha256')

            if not update:
                user = User(email=email, user_name=user_name,
                            password=password, is_admin=is_admin)
                db.session.add(user)
                flash('Usuario cadastrado!', category='success')
            else:
                user.user_name = user_name
                user.email = email
                user.password = password
                user.is_admin = is_admin
                flash('Dados atualizados!', category='success')
            db.session.commit()

    return user
