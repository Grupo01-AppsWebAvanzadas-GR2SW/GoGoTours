from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.application.chat.dtos.send_message_request_dto import SendMessageRequestDto


class ResetPasswordView(MethodView):
    @inject
    def __init__(self, chat_service: ChatServiceAsync):
        self._chat_service = chat_service

    async def get(self):
        return render_template("auth/reset_password.html")
