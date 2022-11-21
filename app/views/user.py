from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__)


@user.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('user/profile.html', title='Perfil')