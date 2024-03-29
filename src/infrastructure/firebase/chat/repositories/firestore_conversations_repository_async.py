from typing import Optional
from google.cloud.firestore import AsyncClient
from google.cloud import firestore
from injector import inject

from src.domain.chat.entities.conversation import Conversation
from src.application.chat.repositories.conversations_repository_async import ConversationsRepositoryAsync
from src.infrastructure.firebase.common.repositories.firestore_generic_repository_async import \
    FirestoreGenericRepositoryAsync


class FirestoreConversationsRepositoryAsync(
    FirestoreGenericRepositoryAsync[Conversation, str],
    ConversationsRepositoryAsync
):
    @inject
    def __init__(self, firestore_client: AsyncClient):
        super().__init__(firestore_client, 'conversations', Conversation)

    async def get_conversation_between_users_async(self, customer_id: str, admin_id: str) -> Optional[Conversation]:
        docs_stream = (
            self._firestore_client.collection('conversations')
            .where(field_path='participants', op_string='==', value=[customer_id, admin_id])
            .stream()
        )

        if docs_stream is not None:
            async for doc in docs_stream:
                conversation = Conversation('', '')
                conversation_dict = doc.to_dict()
                conversation_dict['id'] = doc.id
                conversation.merge_dict(conversation_dict)
                return conversation
        else:
            return None

    async def get_user_conversations_async(self, user_id: str) -> list[Conversation]:
        query = (self._firestore_client.collection('conversations')
                 .order_by('updated_at', direction=firestore.Query.DESCENDING)
                 .where('participants', 'array_contains_any', [user_id]))

        docs_stream = query.stream()
        if docs_stream:
            conversations = []
            async for doc in docs_stream:
                conversation_dict = doc.to_dict()
                conversation_dict['id'] = doc.id
                conversation = Conversation('', '')
                conversation.merge_dict(conversation_dict)
                conversations.append(conversation)
            return conversations
        else:
            return []

    async def get_user_conversation_async(self, user_id: str, conversation_id: str) -> Optional[Conversation]:
        conversation: Optional[Conversation] = await self.get_async(conversation_id)
        if conversation is None:
            return None

        if user_id not in conversation.participants:
            return None

        return conversation
