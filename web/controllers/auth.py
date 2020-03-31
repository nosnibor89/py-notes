from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from notes.models import User, db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif User.query.filter_by(username=username).first():
            error = 'Username already taken'

        if not error:
            hashed_pass = generate_password_hash(password)
            user = User(username=username, password=hashed_pass)
            db.session.add(user)
            db.session.commit()
            flash('Successfully signed up. Please log in', 'success')
            return redirect(url_for('auth.log_in'))

        flash(error, 'error')

    return render_template('sign_up.html')


@bp.route('/login', methods=('GET', 'POST'))
def log_in():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        else:
            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password, password):
                error = 'Incorrect username or password'

        if not error:
            flash('Welcome to the notes app', 'success')
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('notes.notes'))

        flash(error, 'error')

    return render_template('log_in.html')


@bp.route('/logout')
def log_out():
    session.clear()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('auth.log_in'))
