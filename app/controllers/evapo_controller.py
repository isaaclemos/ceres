from datetime import date

import pandas as pd
import plotly.express as px
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app.ext.database import db
from app.models import Information
from app.controllers.user_controller import UserController

class EvapoController:
    before_request=['check_is_authenticated']
    
    def check_is_authenticated(self):
        return UserController.check_is_authenticated(self)
        
    def et_info(self, id):
        
        date_filter = request.form.get('date_filter')
        
        if date_filter and request.method == 'POST':
            return redirect(url_for('evapo.et_info_today', id=id, date_filter=date_filter))
        else:
            return self.et_info_today(id, date_filter)
        
    def et_info_today(self, id, date_filter=None):                
        if not date_filter:
            date_filter = str(date.today())
        df = pd.read_sql_query(db.select(Information).filter(Information.station_id == id,  func.Date(Information.date_time) == date.fromisoformat(date_filter)).order_by('date_time'), db.engine)

        fig = px.line(df, x='date_time', y=['min', 'max', 'mean', 'median', 'std', 'var'], title="Evapotranspiração horaria",
                      labels={'time': 'Hora', 'value': 'Valor', 'variable': 'Informações ET:'}, template='plotly_white')
        fig.update_layout(title_x=0.5, xaxis={'title': ''}, yaxis={'title': ''})

        return render_template('user/evapo_info.html', graphJSON=fig.to_json(), id=id, informations=df, title=f"Evapotranspiração diaria.", date_filter=date_filter)
