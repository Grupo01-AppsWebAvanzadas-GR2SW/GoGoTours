from google.cloud.firestore import AsyncClient
from google.cloud import firestore
from injector import inject
from src.domain.chat.entities.message import Message
from src.infrastructure.firebase.common.repositories.firestore_generic_repository_async import FirestoreGenericRepositoryAsync
from src.application.chat.repositories.messages_repository_async import MessagesRepositoryAsync


class FirestoreMessagesRepositoryAsync(FirestoreGenericRepositoryAsync[Message, str], MessagesRepositoryAsync):
    @inject
    def __init__(self, firestore_client: AsyncClient):
        super().__init__(firestore_client, 'messages', Message)

    async def get_n_latest_messages(self, n: int) -> list[Message]:
        docs_stream = self._firestore_client.collection('messages').order_by(
            'created_at',
            direction=firestore.Query.DESCENDING
        ).limit(n).stream()
        messages = []
        async for doc in docs_stream:
            message_dict = doc.to_dict()
            message_dict["id"] = doc.id
            message = Message()
            message.merge_dict(doc.to_dict())
            messages.append(message)
        return messages
