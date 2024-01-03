from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessageResponseDto:
    text: str
    date_sent: datetime
