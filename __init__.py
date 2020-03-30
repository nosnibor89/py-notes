import os

from flask import Flask, session, g
from flask_migrate import Migrate


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
    from .auth import bp as auth_module
    from .notes import bp as notes_module

    Migrate(app, db)
    db.init_app(app)
    app.register_blueprint(auth_module)
    app.register_blueprint(notes_module)

    @app.before_request
    def load_user():
        user_id = session.get('user_id')

        if user_id:
            g.user = User.query.get(user_id)
        else:
            g.user = None

    return app
