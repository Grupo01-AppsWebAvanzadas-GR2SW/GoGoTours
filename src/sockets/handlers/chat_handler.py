from flask import session
from flask_socketio import join_room
from injector import inject
from socketio import AsyncServer

from src.extensions.decorations_extension import login_required


def register_chats_handlers(socketio: AsyncServer):
    @socketio.on('join_room')
    @inject
    def on_join_room(socket: AsyncServer, conversation_id: str):
        print(f"Joining room {conversation_id}")
        join_room(conversation_id)

    @socketio.on('send_message')
    def on_send_message():
        pass
