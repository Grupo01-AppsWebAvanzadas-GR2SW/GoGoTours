from typing import Dict, Any
from src.domain.common.entities.base_entity import BaseEntity


class Message(BaseEntity[str]):
    def __init__(self, text: str = '', entity_id: str = ''):
        super().__init__(entity_id)
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if not isinstance(value, str):
            raise TypeError('text must be a string')
        if len(value) < 1 or len(value) > 1024:
            raise ValueError('text must be between 1 and 1024 characters')
        self._text = value

    def merge_dict(self, source: Dict[str, Any]) -> None:
        super().merge_dict(source)
        self._text = source["text"] if 'text' in source else ''

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict["text"] = self._text
        return base_dict
