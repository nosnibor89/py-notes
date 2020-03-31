from flask_sqlalchemy import SQLAlchemy
from mistune import markdown

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class User(Base):
    __tablename__ = 'users'

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    notes = db.relationship('Note', backref=db.backref('author', lazy=True))


class Note(Base):
    __tablename__ = 'notes'

    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # user = db.relationship('User', backref=db.backref('notes', lazy=True))

    @property
    def body_html(self):
        return markdown(self.body)
