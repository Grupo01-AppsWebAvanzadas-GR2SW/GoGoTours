from datetime import datetime
from typing import Dict, Any
from src.domain.common.entities.base_entity import BaseEntity
from src.domain.chat.entities.message import Message


class Conversation(BaseEntity[str]):
    def __init__(
            self,
            customer_id: str = '',
            admin_id: str = '',
            entity_id: str = ''
    ):
        super().__init__(entity_id)
        self._participants: list[str] = [customer_id, admin_id]

    @property
    def participants(self) -> list[str]:
        return self._participants

    def merge_dict(self, source: Dict[str, Any]) -> None:
        super().merge_dict(source)
        self._participants = source['participants'] if 'participants' in source else []

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict['participants'] = self._participants
        return base_dict
