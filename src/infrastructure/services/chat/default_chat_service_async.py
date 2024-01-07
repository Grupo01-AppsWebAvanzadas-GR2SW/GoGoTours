from src.domain.chat.entities.message import Message
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.application.chat.dtos.send_message_request_dto import SendMessageRequestDto
from src.application.chat.dtos.chat_message_response_dto import ChatMessageResponseDto
from src.application.chat.repositories.messages_repository_async import MessagesRepositoryAsync
from injector import inject


class DefaultChatServiceAsync(ChatServiceAsync):
    @inject
    def __init__(self, messages_repository_async: MessagesRepositoryAsync):
        self._messages_repository_async = messages_repository_async

    async def get_chat_messages(self) -> list[ChatMessageResponseDto]:
        messages = await self._messages_repository_async.get_n_latest_messages(10)
        return [ChatMessageResponseDto(text=message.text, date_sent=message.created_at) for message in messages]

    async def send_message(self, message: SendMessageRequestDto):
        await self._messages_repository_async.add_async(Message(text=message.message))
