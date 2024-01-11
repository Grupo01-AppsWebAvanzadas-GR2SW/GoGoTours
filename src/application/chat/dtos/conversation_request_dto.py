from dataclasses import dataclass


@dataclass
class ConversationRequestDto:
    user_id: str
    conversation_id: str
