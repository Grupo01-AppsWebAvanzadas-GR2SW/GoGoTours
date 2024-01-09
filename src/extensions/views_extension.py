from flask import abort
from functools import wraps
from src.web.views.chat_view import ChatView
from src.web.views.home_view import HomeView
from src.web.views.package_detail_view import PackageDetailView
from src.web.views.package_add_manager import PackageAddView
from web.views.package_edit_manager import PackageEditView
from web.views.package_search_view import PackageSearchView
from src.web.views.login_view import LoginView
from src.web.views.signup_view import SignupView
from src.web.views.reset_password_view import ResetPasswordView
from flask import session


def is_administrator():
    return session.get('rol') == 'administrador'


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not is_administrator():
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


def register_views(app):
    # Añadir la vista de chat con el decorador admin_required
    app.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
    app.add_url_rule('/home', view_func=HomeView.as_view('home'))
    app.add_url_rule('/package_detail/<string:name>', view_func=PackageDetailView.as_view('package_detail'))
    app.add_url_rule('/edit_package/<string:name>', view_func=PackageEditView.as_view('edit_package'))
    app.add_url_rule('/addPackage', view_func=PackageAddView.as_view('add_package'))
    app.add_url_rule('/package_search', view_func=PackageSearchView.as_view('package_search'))

    app.add_url_rule('/login', view_func=LoginView.as_view('login'))
    app.add_url_rule('/signup', view_func=SignupView.as_view('signup'))
    app.add_url_rule('/reset-password', view_func=ResetPasswordView.as_view('reset-password'))
