from flask import Blueprint, render_template, request, redirect , url_for, abort
from flask_login import current_user
from ..models.user import User
from ..models.station import Station

admin = Blueprint('admin', __name__)

@admin.before_request
def check_admin():    
    if not current_user.is_admin :
        return abort(403)

@admin.route('/user', methods=['GET', 'POST'])
def user():    
    users = User.query.all()
    return render_template('admin/user.html', title='Usuarios', users=users)

@admin.route('/station/user/<int:id>', methods=['GET'])
def station(id):
    user=User.query.get(id)    
    return render_template('admin/station.html', title='Estações',user=user)

@admin.route('/user/edit/<int:id>', methods=['GET'])
def edit_user(id):  
    user=User.query.get(id)  
    return render_template('admin/form_user.html', title='Usuario', user=user)

@admin.route('/station/edit/<int:id>', methods=['GET'])
def edit_station(id):    
    station=Station.query.get(id)  
    return render_template('admin/form_station.html', title='Estação', station=station)

@admin.route('/station/user/<int:id>/new', methods=['GET'])
def new_station(id):        
    return render_template('admin/form_station.html', title='Estação')
