from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.application.chat.dtos.send_message_request_dto import SendMessageRequestDto


class ChatView(MethodView):
    @inject
    def __init__(self, chat_service: ChatServiceAsync):
        self._chat_service = chat_service

    async def get(self):
        messages = await self._chat_service.get_chat_messages()
        messages.reverse()
        return render_template("chat/chat.html", messages=messages)

    async def post(self):
        message = request.form.get("message")
        message_dto = SendMessageRequestDto(message=message)
        await self._chat_service.send_message(message_dto)
        return redirect(url_for("chat"))
