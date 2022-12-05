import pandas as pd
from datetime import datetime
import plotly.express as px
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from app.ext.database import db
from app.models import Information, User

user_bp = Blueprint('user', __name__,url_prefix='/user')

@user_bp.before_request
@login_required
def check_admin():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@user_bp.route('/index', methods=['GET'])
def index():

    df=pd.read_sql_query(db.select(Information).filter(Information.station_id==1), db.engine)

    fig=px.line(df,x='datetime',y=['min','max','mean','median','std','var'],title="Evapotranspiração horaria",
    labels={'time':"Hora", 'value': 'Valor', 'variable':'Informações ET:'},template='plotly_white')    
    fig.update_layout(title_x=0.5, xaxis={'title':'Hora'} ,yaxis={'title':''})
    return render_template('home.html',graphJSON=fig.to_json(), data=df, title =f"Evaportranspiração de {df['datetime'][0].date().strftime('%d/%m/%Y')}")

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

