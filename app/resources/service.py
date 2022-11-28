from flask import Blueprint, request, jsonify, make_response
from app.database import db
from app.models import Station
from datetime import datetime

service_bp = Blueprint('service', __name__)

@service_bp.route('/receive', methods=['GET', 'POST'])
def get_data():
    content = request.json
    station = Station.query.filter_by(
        mac_address=content['mac_address']).first()
    t = datetime.strptime('2021-01-04 22:00', '%Y-%m-%d %H:%M')


    if station:
        return jsonify(t=str(t))
    else:
        return make_response('{}', 403)