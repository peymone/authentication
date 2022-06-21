from flask import Blueprint, render_template, current_app, redirect, request, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from .mail import send_email
from .db import get_db


blueprint = Blueprint('auth', __name__)


def generate_confirmation_token(email):
    seializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return seializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    serialilez = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serialilez.loads(
        token, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    return email


@blueprint.route('/')
@blueprint.route('/signin', methods=['GET', 'POST'])
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

            if user[1] == 'False':
                flash("Please, confirm your email address", category='error')
                return render_template('signin.html', signup_link=url_for('.signup'))

            if error is None:
                if request.form.get('rememberMe') is None:
                    return "<h1>Content here</h1>"
                else:
                    session.clear()
                    session['logged_in'] = True
                    return "<h1>Content here and I'm have cookie!</h1>"

                    # return redirect(url_for('content'))

            flash(error, category='error')
            return render_template('signin.html', signup_link=url_for('.signup'))

        else:
            return render_template('signin.html', signup_link=url_for('.signup'))


@blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email, login, password = request.form['email'], request.form['login'], request.form['password']

        db = get_db()
        try:
            db.execute("insert into users values (?, ?, ?, ?)",
                       (email.lower(), 'False', login.lower(), generate_password_hash(password)))
            flash("You are signed up, confirm your email", category='success')
        except db.IntegrityError:
            flash(f"User {login} is already registred", category='error')

        db.commit()

        token = generate_confirmation_token(email)
        confirm_url = url_for('.confirm_email', token=token, _external=True)

        send_email(
            f"Welcome, {login.title()}! Thanks for signed up. Plesase follow this link to activate your account\n{confirm_url}")
        return render_template('signup.html', signin_link=url_for('.signin'))
    else:
        return render_template('signup.html', signin_link=url_for('.signin'))


@blueprint.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    db = get_db()

    if db.execute("select * from users where email = ?", [email]).fetchone() is None:
        return "<h1>your tocen is incorrect</h1>"
    else:
        db.execute(
            "update users set confirmed_email = ? where email = ?", ['True', email])

        db.commit()
        return "<h1>your login is confirmed now</h1>"
        # return render_template('confirm_email.html')


@blueprint.route('/content')
def content():
    if session.get('logged_in'):
        return render_template('content.html')
    else:
        return redirect(url_for('login'))


@blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('.signin'))
