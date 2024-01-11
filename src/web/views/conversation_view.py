from flask import session, render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject

from src.application.chat.dtos.conversation_request_dto import ConversationRequestDto
from src.application.chat.dtos.conversation_response_dto import ConversationResponseDto
from src.application.chat.dtos.send_message_request_dto import SendMessageRequestDto
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.extensions.decorations_extension import login_required_async


class ConversationView(MethodView):
    @inject
    def __init__(self, chat_service: ChatServiceAsync):
        self._chat_service = chat_service

    @login_required_async
    async def get(self, conversation_id: str):
        user_id = session.get("id")
        conversation: ConversationResponseDto = await self._chat_service.get_conversation_async(
            ConversationRequestDto(user_id=user_id, conversation_id=conversation_id)
        )
        conversations_summaries = await self._chat_service.get_user_conversations_summaries_async(user_id)
        return render_template(
            "chat/conversations.html",
            conversation=conversation,
            conversations_summaries=conversations_summaries
        )

    @login_required_async
    async def post(self, conversation_id: str):
        user_id = session.get("id")
        message = request.form.get("message")
        if not message:
            return redirect(url_for('chat_conversation', conversation_id=conversation_id))
        user_id = session.get("id")
        await self._chat_service.send_message_async(
            SendMessageRequestDto(
                sender_id=user_id,
                conversation_id=conversation_id,
                message=message
            )
        )
        return redirect(url_for('chat_conversation', conversation_id=conversation_id))
