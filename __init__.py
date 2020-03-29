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

    from .models import db
    from .auth import bp as auth_module
    Migrate(app, db)
    db.init_app(app)

    app.register_blueprint(auth_module)

    @app.route('/')
    def notes():
        if not session.get('user_id'):
            return redirect(url_for('auth.log_in'))

        return 'Notes view'

    return app
