from flask import Blueprint, render_template
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route("/")
@login_required
def index():
    return render_template("home.html", title='Home')
