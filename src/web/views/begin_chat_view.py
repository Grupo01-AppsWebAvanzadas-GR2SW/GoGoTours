from flask import abort, redirect, url_for

from flask import session, request, render_template
from flask.views import MethodView
from injector import inject

from src.application.chat.dtos.begin_chat_request_dto import BeginChatRequestDto
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.extensions.decorations_extension import admin_forbidden_async, login_required_async


class BeginChatView(MethodView):
    @inject
    def __init__(self, chat_service: ChatServiceAsync):
        self._chat_service = chat_service

    @login_required_async
    @admin_forbidden_async
    async def get(self):
        try:
            user_id: str = session.get("id")
            admin_id: str = request.args.get("admin_id")
            conversation = await self._chat_service.begin_chat_async(
                BeginChatRequestDto(customer_id=user_id, admin_id=admin_id))
            return redirect(url_for('chat_conversation', conversation_id=conversation.conversation_id))
        except ValueError:
            abort(404)
