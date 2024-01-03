from dataclasses import dataclass


@dataclass
class SendMessageRequestDto:
    message: str
