from typing import Optional
from datetime import datetime
import uuid


class BaseEntity:
    def __init__(self):
        self._id: str = str(uuid.uuid4())
        self._created_at: datetime = datetime.now()
        self._updated_at: Optional[datetime] = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update(self) -> None:
        self._updated_at = datetime.now()
