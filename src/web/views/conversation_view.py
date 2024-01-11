from flask import session, render_template
from flask.views import MethodView
from injector import inject

from src.application.chat.dtos.conversation_request_dto import ConversationRequestDto
from src.application.chat.dtos.conversation_response_dto import ConversationResponseDto
from src.application.chat.services.chat_service_async import ChatServiceAsync


class ConversationView(MethodView):
    @inject
    def __init__(self, chat_service: ChatServiceAsync):
        self._chat_service = chat_service

    async def get(self, conversation_id: str):
        user_id = session.get("id")
        conversation: ConversationResponseDto = await self._chat_service.get_conversation_async(
            ConversationRequestDto(user_id=user_id, conversation_id=conversation_id)
        )
        
        return render_template(
            "chat/conversations.html",
            conversation=conversation,

        )

    async def post(self, conversation_id: str):
        pass
