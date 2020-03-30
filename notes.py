from flask import (
    Blueprint, request, flash, render_template, redirect, g, url_for
)

from .models import db, Note
from .util import requires_login

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/', methods=['GET'])
@requires_login
def notes():
    return render_template('note_index.html')


@bp.route('/create', methods=['GET', 'POST'])
@requires_login
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if not error:
            user = g.user
            print(user)
            user.notes.append(
                Note(title=title, body=body)
            )
            db.session.commit()
            flash(f'Notes {title} was created successfully', 'success')
            return redirect(url_for('notes.notes'))

        flash(error, 'error')

    return render_template('note_create.html')
