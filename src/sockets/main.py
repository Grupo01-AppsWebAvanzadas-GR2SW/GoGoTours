from socketio import AsyncServer

from src.sockets.handlers.chat_handler import register_chats_handlers


def register_handlers(socketio: AsyncServer):
    register_chats_handlers(socketio)
