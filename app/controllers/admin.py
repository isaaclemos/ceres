from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
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


@admin_bp.route('/user/store', methods=['POST'])
def user_store():
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

    return redirect(url_for('admin.user'))


@admin_bp.route('/user/<int:id>/station', methods=['GET'])
def stations_by_user(id):
    user = User.query.get(id)
    return render_template('admin/station.html', title='Estações', stations=user.stations, user=user)


@admin_bp.route('/user/<int:id>/station/store', methods=['POST'])
def station_store(id):

    station = Station()
    station.user_id = id
    station.mac_address = request.form.get('mac_address')
    station.altitude = request.form.get('altitude')
    station.altura = request.form.get('altura')
    station.altura_dossel = request.form.get('altura_dossel')
    station.latitude = request.form.get('latitude')
    station.longitude = request.form.get('longitude')
    station.cod_inmet = request.form.get('cod_inmet')

    db.session.add(station)
    db.session.commit()

    return redirect(url_for('admin.stations_by_user', id=id))


@admin_bp.route('/user/<int:id>/station/<int:id_station>/delete', methods=['GET'])
def station_delete(id, id_station):

    station = Station.query.get(id_station)
    db.session.delete(station)
    db.session.commit()

    return redirect(url_for('admin.stations_by_user', id=id))


@admin_bp.route('user/<int:id>/station/<int:id_station>/edit', methods=['GET', 'POST'])
def edit_station(id, id_station):

    station = Station.query.get(id_station)

    if request.method == 'POST':
        station.user_id = id
        station.mac_address = request.form.get('mac_address')
        station.altitude = request.form.get('altitude')
        station.altura = request.form.get('altura')
        station.altura_dossel = request.form.get('altura_dossel')
        station.latitude = request.form.get('latitude')
        station.longitude = request.form.get('longitude')
        station.cod_inmet = request.form.get('cod_inmet')
        db.session.commit()
        return redirect(url_for('admin.stations_by_user', id=id))

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

            if not update:
                user = User(email=email, user_name=user_name,
                            password=password1, is_admin=is_admin)
                db.session.add(user)
                flash('Usuario cadastrado!', category='success')
            else:
                user.user_name = user_name
                user.email = email
                user.set_password(password1)
                user.is_admin = is_admin
                flash('Dados atualizados!', category='success')
            db.session.commit()

    return user
