from flask_injector import FlaskInjector
from injector import singleton, Binder
from google.cloud.firestore import AsyncClient
from src.application.chat.repositories.messages_repository_async import MessagesRepositoryAsync
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.infrastructure.firebase.chat.repositories.firestore_messages_repository_async import \
    FirestoreMessagesRepositoryAsync
from src.infrastructure.services.chat.default_chat_service_async import DefaultChatServiceAsync
from src.infrastructure.firebase.config.config import get_firestore_async


def configure_binding(binder: Binder) -> Binder:
    binder.bind(AsyncClient, to=get_firestore_async, scope=singleton)
    binder.bind(MessagesRepositoryAsync, to=FirestoreMessagesRepositoryAsync, scope=singleton)
    binder.bind(ChatServiceAsync, to=DefaultChatServiceAsync, scope=singleton)
    return binder


def register_dependency_injection(app) -> None:
    FlaskInjector(app=app, modules=[configure_binding])
