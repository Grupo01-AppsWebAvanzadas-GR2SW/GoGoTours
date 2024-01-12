from typing import Optional

from google.cloud.firestore import AsyncClient
from google.cloud import firestore
from injector import inject

from src.application.chat.repositories.messages_repository_async import MessagesRepositoryAsync
from src.domain.chat.entities.message import Message
from src.infrastructure.firebase.common.repositories.firestore_generic_repository_async import \
    FirestoreGenericRepositoryAsync


class FirestoreMessagesRepositoryAsync(
    FirestoreGenericRepositoryAsync[Message, str],
    MessagesRepositoryAsync
):
    @inject
    def __init__(self, firestore_client: AsyncClient):
        super().__init__(firestore_client, 'messages', Message)

    async def get_messages_for_conversation_async(self, conversation_id: str) -> list[Message]:
        docs_stream = (
            self._firestore_client.collection('messages')
            .where('conversation_id', '==', conversation_id)
            .order_by('created_at', direction=firestore.Query.ASCENDING)
        ).stream()

        messages = []
        async for doc in docs_stream:
            message = Message()
            message_dict = doc.to_dict()
            message_dict['id'] = doc.id
            message.merge_dict(message_dict)
            messages.append(message)
        return messages

    async def get_last_message_for_conversation_async(self, conversation_id: str) -> Optional[Message]:
        docs_stream = (
            self._firestore_client.collection('messages')
            .where('conversation_id', '==', conversation_id)
            .order_by('created_at', direction=firestore.Query.DESCENDING)
        ).limit(1).stream()

        async for doc in docs_stream:
            message = Message()
            message_dict = doc.to_dict()
            message_dict['id'] = doc.id
            message.merge_dict(message_dict)
            return message
        return None
