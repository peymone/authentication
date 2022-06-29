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
    if session.get('stay_in'):
        return redirect(url_for('.content'))
    session.clear()

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
        else:
            if user[1] == 'False':
                flash("Please, confirm your email address", category='error')
                return render_template('signin.html', signup_link=url_for('.signup'))

        if error is None:
            if request.form.get('rememberMe') is None:
                session['logged_in'] = True
                session['stay_in'] = False
                return redirect(url_for('.content'))

            else:
                session['logged_in'] = True
                session['stay_in'] = True
                return redirect(url_for('.content'))

        flash(error, category='error')
        return render_template('signin.html', signup_link=url_for('.signup'), forgot_link=url_for('.forgot_main'))

    else:
        return render_template('signin.html', signup_link=url_for('.signup'), forgot_link=url_for('.forgot_main'))


@blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if session.get('stay_in'):
        return redirect(url_for('.content'))
    session.clear()

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
            f"Welcome, {login.title()}! Thanks for signed up. Please follow this link to activate your account:\n{confirm_url}", subject='Password confirmation', recipients=[email.lower()])
        return render_template('signup.html', signin_link=url_for('.signin'))
    else:
        return render_template('signup.html', signin_link=url_for('.signin'))


@blueprint.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    db = get_db()

    if db.execute("select * from users where email = ?", [email]).fetchone() is None:
        return "<h1>your token is incorrect</h1>"
    else:
        db.execute(
            "update users set confirmed_email = ? where email = ?", ['True', email])

        db.commit()
        return render_template('confirm_email.html', email=email, signin_link=url_for('.signin'))


@blueprint.route('/forgot', methods=['POST', 'GET'])
def forgot_main():
    if session.get('stay_in'):
        return redirect(url_for('.content'))
    session.clear()

    if request.method == 'POST':
        token = generate_confirmation_token(request.form['email'])
        forgot_url = url_for('.forgot_password', token=token, _external=True)

        flash("Follow the link in the email to reset your password",
              category='success')
        send_email(
            f"Please, follow this link to reset your password:\n{forgot_url}", subject='Recovery password', recipients=[request.form['email']])

        return render_template('forgot_main.html', signin_link=url_for('.signin'))
    else:
        return render_template('forgot_main.html', signin_link=url_for('.signin'))


@blueprint.route('/forgot/<token>', methods=['POST', 'GET'])
def forgot_password(token):
    email = confirm_token(token)
    if request.method == 'POST':
        db = get_db()

        if db.execute("select * from users where email = ?", [email]).fetchone() is None:
            return "<h1>your token is incorrect</h1>"
        else:
            db.execute("update users set password = ? where email = ?",
                       [generate_password_hash(request.form['password']), email])

            db.commit()
            flash("Your password has been changed!", category='success')
            return render_template('forgot_password.html', signin_link=url_for('.signin'), email=email, token=token)
    else:
        return render_template('forgot_password.html', signin_link=url_for('.signin'), email=email, token=token)


@blueprint.route('/content')
def content():
    if session.get('logged_in'):
        return render_template('content.html', logout_link=url_for('.logout'))
    else:
        return redirect(url_for('.signin'))


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.signin'))
