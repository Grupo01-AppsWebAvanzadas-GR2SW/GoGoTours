from abc import ABC, abstractmethod
from src.application.chat.dtos.send_message_request_dto import SendMessageRequestDto
from src.application.chat.dtos.chat_message_response_dto import ChatMessageResponseDto


class ChatServiceAsync(ABC):
    @abstractmethod
    async def get_chat_messages(self) -> list[ChatMessageResponseDto]:
        pass

    @abstractmethod
    async def send_message(self, message: SendMessageRequestDto):
        pass
