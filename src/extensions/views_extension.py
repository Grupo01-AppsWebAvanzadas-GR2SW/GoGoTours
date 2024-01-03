from src.web.views.chat_view import ChatView


def register_views(app):
    app.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
