from src.web.views.chat_view import ChatView
from src.web.views.home_view import HomeView


def register_views(app):
    app.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
    app.add_url_rule('/home', view_func=HomeView.as_view('home'))
