from flask import (
    Blueprint, request, flash, render_template, redirect, g, url_for
)

from notes.models import db, Note
from notes.web.middlewares import requires_login

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/', methods=['GET'])
@requires_login
def notes():
    user_notes = g.user.notes
    return render_template('note_index.html', notes=user_notes)


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
            user.notes.append(
                Note(title=title, body=body)
            )
            db.session.commit()
            flash(f'Note "{title}" was created successfully', 'success')
            return redirect(url_for('notes.notes'))

        flash(error, 'error')

    return render_template('note_create.html')


@bp.route('/<int:note_id>/edit', methods=['GET', 'PATCH', 'POST'])
@requires_login
def edit(note_id):
    note = Note.query.filter_by(user_id=g.user.id, id=note_id).first_or_404()
    if request.method in ['PATCH', 'POST']:
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if not error:
            note.title = title
            note.body = body
            db.session.commit()
            flash(f'Note "{title}" was updatedd successfully', 'success')
            return redirect(url_for('notes.notes'))

        flash(error, 'error')

    return render_template('note_update.html', note=note)


@bp.route('/<int:note_id>/delete', methods=['DELETE', 'GET'])
@requires_login
def delete(note_id):
    note = Note.query.filter_by(user_id=g.user.id, id=note_id).first_or_404()
    db.session.delete(note)
    db.session.commit()

    flash(f"Successfully deleted note: '{note.title}'", 'success')
    return redirect(url_for('notes.notes'))
