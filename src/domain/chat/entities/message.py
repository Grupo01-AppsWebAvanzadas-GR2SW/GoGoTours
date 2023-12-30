from domain.common.entities.base_entity import BaseEntity


class Message(BaseEntity):
    def __init__(self, text: str):
        super().__init__()
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
