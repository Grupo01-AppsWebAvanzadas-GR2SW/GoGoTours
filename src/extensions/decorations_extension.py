from flask import session
from flask import abort
from functools import wraps


def is_administrator():
    return bool(session.get('is_admin')) == True


def admin_required(func: object) -> object:
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not is_administrator():
            abort(403)
        return func(*args, **kwargs)

    return decorated_view
