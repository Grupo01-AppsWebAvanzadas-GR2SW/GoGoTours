from abc import ABC, abstractmethod
from src.domain.chat.entities.message import Message
from src.application.common.repositories.generic_repository_async import GenericRepositoryAsync


class MessagesRepositoryAsync(GenericRepositoryAsync[Message, str], ABC):
    @abstractmethod
    async def get_n_latest_messages(self, n: int) -> list[Message]:
        pass
