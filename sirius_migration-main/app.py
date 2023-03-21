from flask import Flask, render_template, url_for, flash
from flask import request, redirect
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

con = sqlite3.connect("test.db", check_same_thread=False)
cur = con.cursor()

#cur.execute("DROP TABLE IF EXISTS users")
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT NOT NULL,
    password  TEXT)""")
con.commit()


def addtotable(username, password):
    cur.execute(f"SELECT username, password FROM users WHERE username = '{username}'")
    if cur.fetchone() is None:
        cur.execute(f"INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
        con.commit()
        return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user')
def user():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))
    return 'user page: ' + username + '-' + str(password)


@app.route('/registration', methods=['get', 'post'])
def reg():
    if request.method == "POST":
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        res = addtotable(username, password)
        if res:
            flash("Вы успешно зарегестрировались!", "success")
            return redirect(url_for('auth'))
        else:
            flash("Ошибка при добавлении в базу!", "error")
    return render_template("registration.html")


@app.route('/auth', methods=['get', 'post'])
def auth():
    if request.method == "POST":
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        return render_template('user.html', username=username, password=password)
    elif request.method == "GET":
        return render_template('auth.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
