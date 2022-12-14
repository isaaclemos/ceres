import os
from datetime import date

import pandas as pd
import plotly.express as px
from flask import (redirect, render_template, request, send_from_directory,
                   url_for)
from flask_login import current_user, login_required
from sqlalchemy import func

from app.controllers.user_controller import UserController
from app.ext.database import db
from app.models import Information, Station


class EvapoController:
    before_request = ['check_is_authenticated']

    @login_required
    def check_is_authenticated(self):
        return UserController.check_is_authenticated(self)

    def et_info(self, id):

        date_filter = request.form.get('date_filter')

        return redirect(url_for('evapo.et_info_today', id=id, date_filter=date_filter))

    def et_info_today(self, id, date_filter):

        station = Station.query.filter_by(
            id=id, user_id=current_user.id).first()

        if not date_filter:
            date_filter = date.today()
            
        if station:
            query = db.select(Information).where(Information.station_id == id, func.Date(
                Information.date_time) == date_filter).order_by('date_time')

            df = pd.read_sql_query(query, db.engine)

            y = ['min', 'max', 'mean', 'median', 'std', 'var']
            labels = {'time': 'Hora', 'value': 'valor',
                      'variable': 'Variavel'}
            title = "Evapotranspiração horaria"

            fig = px.line(df, x='date_time', y=y, title=title,
                          labels=labels, template='plotly_white')
            fig.update_layout(title_x=0.5, xaxis={
                              'title': ''}, yaxis={'title': ''})

            return render_template('user/evapo_info.html', graphJSON=fig.to_json(), id=id, informations=df, title=title, date_filter=date_filter)
        else:
            return redirect(url_for('station.station'))

    def show_image(self, name=None):
        path = os.path.abspath("station_files")
        return send_from_directory(path, name)
