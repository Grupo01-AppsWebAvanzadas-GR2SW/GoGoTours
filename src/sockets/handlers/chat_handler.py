from flask import session
from flask_socketio import join_room
from injector import inject
from socketio import AsyncServer

from src.extensions.decorations_extension import login_required


def register_chats_handlers(socketio: AsyncServer):
    @socketio.on('join_room')
    @login_required
    @inject
    def on_join_room(conversation_id: str):
        user_id = session['id']
        join_room(conversation_id)

    @socketio.on('send_message')
    def on_send_message():
        pass
