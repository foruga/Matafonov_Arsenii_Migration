import os
import sqlite3

from flask import Flask, render_template, request, g, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin

from FDatabase import FDatabase

# Configuration
DATABASE = 'data.db'
DEBUG = True
SECRET_KEY = '`}>j&8D(T81q,L*-#}Jv$UWHOgvo~'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'data.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):
    print('load_user')
    return UserLogin().fromDB(id, dbase)


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    # Linking db if not linked
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDatabase(db)


@app.teardown_appcontext
def close_db(error):
    # Closing the link if linked
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user')
@login_required
def user():
    return render_template('user.html')


@app.route('/registration', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        if len(request.form['email']) > 4 and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['email'], hash)
            if res:
                flash('Вы успешно зарегестрировались!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в базу данных', 'error')
        else:
            flash('Неверно заполнены поля!', 'error')
    return render_template('registration.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for(user))
        flash("Неверная пара логин/пароль", 'error')
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
