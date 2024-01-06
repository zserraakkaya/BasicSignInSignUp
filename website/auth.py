from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Signed in successfully')
                login_user(user)
                return redirect(url_for('views.dashboard'))
        else:
            flash('Wrong email or password')
    data = request.form
    return render_template('signin.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('This email address already exists.')
        elif(password1 != password2):
            flash('Passwords do not match.')
        elif(len(password1) < 8):
            flash('Password must be at least 8 characters long.')
        else:
            new_user = User(email=email, fname=fname, lname=lname, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            flash('Your account has been created!')
            return redirect(url_for('views.dashboard'))

    return render_template('signup.html', user=current_user)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))