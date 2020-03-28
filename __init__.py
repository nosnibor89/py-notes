import os

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI', default='sqlite:///tmp/test.db')
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db, User
    Migrate(app, db)
    db.init_app(app)

    @app.route('/signup', methods=('GET', 'POST'))
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
                return redirect(url_for('log_in'))

            flash(error, 'error')

        return render_template('sign_up.html')

    @app.route('/login', methods=('GET', 'POST'))
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
                return redirect(url_for('notes'))

            flash(error, 'error')

        return render_template('log_in.html')

    @app.route('/logout')
    def log_out():
        session.clear()
        flash('Successfully logged out.', 'success')
        return redirect(url_for('log_in'))

    @app.route('/')
    def notes():
        if not session.get('user_id'):
            return redirect(url_for('log_in'))

        return 'Notes view'

    return app
