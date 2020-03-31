import functools
from flask import redirect, url_for, g


def requires_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.log_in'))
        else:
            return view(**kwargs)

    return wrapped_view
