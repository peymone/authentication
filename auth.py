from winreg import REG_QWORD
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os


DEBUG = True
USERNAME = 'admin'
PASSWORD = 'default'
DATABASE = '/tmp/auth.db'
SECRET_KEY = 'development key'      # change for production

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='default',
    SECRET_KEY='development key',
    DATABASE=os.path.join(app.root_path, 'auth.db')

))
app.config.from_envvar('AUTH_SETTINGS', silent=True)


def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    # connection.row_factory = sqlite3.Row

    return connection


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as file:
            db.cursor().executescript(file.read().decode('utf8'))

        db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


@app.teardown_appcontext
def close_db(eror):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get('logged_in'):
        return "<h1>Content here</h1>"
        # return redirect(url_for('content'))
    else:
        if request.method == 'POST':
            error = None
            db = get_db()
            if '@' in request.form['login']:
                user = db.execute(
                    "select * from users where email = ?", [request.form['login'].lower()]).fetchone()
            else:
                user = db.execute(
                    "select * from users where login = ?", [request.form['login'].lower()]).fetchone()

            if user is None:
                error = "Incorrect login"
            elif not check_password_hash(user[-1], request.form['password']):
                error = "Incorrect password"

            if error is None:
                if request.form.get('rememberMe') is None:
                    return "<h1>Content here</h1>"
                else:
                    session.clear()
                    session['logged_in'] = True
                    return "<h1>Content here and I'm have cookie!</h1>"

                    # return redirect(url_for('content'))

            flash(error, category='error')
            return render_template('signin.html', signup_link=url_for('signup'))

        else:
            return render_template('signin.html', signup_link=url_for('signup'))


@ app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email, login, password = request.form['email'], request.form['login'], request.form['password']

        db = get_db()
        try:
            db.execute("insert into users values (?, ?, ?)",
                       (email.lower(), login.lower(), generate_password_hash(password)))
            flash("You are signed up", category='success')
        except sqlite3.IntegrityError:
            flash(f"User {login} is already registred", category='error')

        db.commit()
        return render_template('signup.html', signin_link=url_for('signin'))

    else:
        return render_template('signup.html', signin_link=url_for('signin'))


@ app.route('/content')
def content():
    if session.get('logged_in'):
        return render_template('content.html')
    else:
        return redirect(url_for('login'))


@ app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run()
