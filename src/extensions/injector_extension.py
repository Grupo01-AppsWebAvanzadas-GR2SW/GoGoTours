from flask_injector import FlaskInjector
from injector import singleton, Binder
from google.cloud.firestore import AsyncClient

from src.application.auth.repositories.users_repository_async import UsersRepositoryAsync
from src.application.auth.services.login_service_async import LoginServiceAsync
from src.application.auth.services.signup_service_async import SignupServiceAsync
from src.application.chat.repositories.messages_repository_async import MessagesRepositoryAsync
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.infrastructure.firebase.config.config import get_firestore_async
from src.infrastructure.firebase.auth.repositories.firestore_users_repository_async import FirestoreUsersRepositoryAsync
from src.infrastructure.services.auth.default_login_service_async import DefaultLoginServiceAsync
from src.infrastructure.services.auth.default_signup_service_async import DefaultSignupServiceAsync
from src.infrastructure.services.chat.default_chat_service_async import DefaultChatServiceAsync
from src.infrastructure.firebase.chat.repositories.firestore_messages_repository_async import \
    FirestoreMessagesRepositoryAsync


def configure_binding(binder: Binder) -> Binder:
    binder.bind(AsyncClient, to=get_firestore_async, scope=singleton)
    binder.bind(MessagesRepositoryAsync, to=FirestoreMessagesRepositoryAsync, scope=singleton)
    binder.bind(ChatServiceAsync, to=DefaultChatServiceAsync, scope=singleton)
    binder.bind(UsersRepositoryAsync, to=FirestoreUsersRepositoryAsync, scope=singleton)
    binder.bind(LoginServiceAsync, to=DefaultLoginServiceAsync, scope=singleton)
    binder.bind(SignupServiceAsync, to=DefaultSignupServiceAsync, scope=singleton)
    return binder


def register_dependency_injection(app) -> None:
    FlaskInjector(app=app, modules=[configure_binding])
