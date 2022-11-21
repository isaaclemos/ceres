from flask import Blueprint, render_template, url_for, redirect

bp = Blueprint('', __name__)

@bp.route("/")
def login():
    return render_template("login.html")

@bp.route('/logout', methods=['GET'])
def logout():    
    return redirect(url_for('home'))

@bp.route("/home")
def home():
    return render_template("home.html", title='Home', url=url_for('home'))

@bp.route('/user', methods=['GET'])
def user():    
    return render_template('user.html', title='Usuarios', url=url_for('user'))

@bp.route('/station/<int:id>', methods=['GET'])
def station(id):    
    return render_template('station.html', title='Estações', url=url_for('station', id=id))

@bp.route('/user/edit/<int:id>', methods=['GET'])
def form_user(id):    
    return render_template('form_user.html', title='Usuario', url=url_for('form_user',id=id))

@bp.route('/station/edit/<int:id>', methods=['GET'])
def form_station(id):    
    return render_template('form_station.html', title='Estação', url=url_for('form_station',id=id))

@bp.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', title='Perfil')