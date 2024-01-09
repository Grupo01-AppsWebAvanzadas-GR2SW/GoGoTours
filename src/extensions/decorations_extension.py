import functools

from flask import session
from flask import abort
from functools import wraps


def is_administrator():
    return bool(session.get('is_admin')) is True


def admin_required(func: object) -> object:
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not is_administrator():
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


def admin_required_async(func):
    @functools.wraps(func)
    async def decorated_view_async(*args, **kwargs):
        if not is_administrator():  # Assuming is_administrator_async is an async function
            abort(403)
        return await func(*args, **kwargs)

    return decorated_view_async