from abc import ABC, abstractmethod
from typing import Optional

from src.application.common.repositories.generic_repository_async import GenericRepositoryAsync
from src.domain.chat.entities.message import Message


class MessagesRepositoryAsync(GenericRepositoryAsync[Message, str], ABC):
    @abstractmethod
    async def get_messages_for_conversation_async(self, conversation_id: str) -> list[Message]:
        pass

    @abstractmethod
    async def get_last_message_for_conversation_async(self, conversation_id: str) -> Optional[Message]:
        pass