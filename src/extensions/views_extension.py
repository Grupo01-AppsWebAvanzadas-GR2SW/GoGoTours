from src.web.views.chat_view import ChatView
from src.web.views.home_view import HomeView
from src.web.views.package_detail_view import PackageDetailView


def register_views(app):
    app.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
    app.add_url_rule('/home', view_func=HomeView.as_view('home'))
    app.add_url_rule('/package_detail/<string:name>', view_func=PackageDetailView.as_view('package_detail'))
