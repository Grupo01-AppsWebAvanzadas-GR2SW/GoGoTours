from typing import Optional

from injector import inject

from src.application.auth.repositories.users_repository_async import UsersRepositoryAsync
from src.application.chat.dtos.begin_chat_request_dto import BeginChatRequestDto
from src.application.chat.dtos.conversation_request_dto import ConversationRequestDto
from src.application.chat.dtos.conversation_response_dto import ConversationResponseDto
from src.application.chat.dtos.conversation_summary_response_dto import ConversationSummaryResponseDto
from src.application.chat.dtos.message_response_dto import MessageResponseDto
from src.application.chat.dtos.send_message_request_dto import SendMessageRequestDto
from src.application.chat.repositories.conversations_repository_async import ConversationsRepositoryAsync
from src.application.chat.repositories.messages_repository_async import MessagesRepositoryAsync
from src.application.chat.services.chat_service_async import ChatServiceAsync
from src.domain.chat.entities.conversation import Conversation
from src.domain.chat.entities.message import Message


class DefaultChatServiceAsync(ChatServiceAsync):
    @inject
    def __init__(
            self,
            conversations_repository_async: ConversationsRepositoryAsync,
            messages_repository_async: MessagesRepositoryAsync,
            user_repository_async: UsersRepositoryAsync
    ):
        self._conversations_repository_async = conversations_repository_async
        self._messages_repository_async = messages_repository_async
        self._user_repository_async = user_repository_async

    async def begin_chat_async(self, request: BeginChatRequestDto) -> ConversationResponseDto:
        possible_conversation: Optional[
            Conversation] = await self._conversations_repository_async.get_conversation_between_users_async(
            request.customer_id, request.admin_id
        )

        admin_account = await self._user_repository_async.get_async(request.admin_id)
        if admin_account is None:
            raise ValueError("Administrator not found")

        if possible_conversation is not None:
            return ConversationResponseDto(
                conversation_id=possible_conversation.id,
                recipient_name=admin_account.username,
                messages=[
                    MessageResponseDto(
                        text=message.text,
                        date_sent=message.created_at,
                        sender_id=message.sender_id
                    )
                    for message in await self._messages_repository_async.get_messages_for_conversation_async(
                        possible_conversation.id
                    )
                ]
            )

        new_conversation = Conversation(customer_id=request.customer_id, admin_id=request.admin_id)
        await self._conversations_repository_async.add_async(new_conversation)
        new_conversation = await self._conversations_repository_async.get_conversation_between_users_async(
            request.customer_id, request.admin_id
        )
        return ConversationResponseDto(
            conversation_id=new_conversation.id,
            recipient_name=admin_account.username,
            messages=[]
        )

    async def get_user_conversations_summaries_async(self, user_id: str) -> list[ConversationSummaryResponseDto]:
        conversation_summaries: list[ConversationSummaryResponseDto] = []
        for conversation in await self._conversations_repository_async.get_user_conversations_async(user_id):
            recipient_id = conversation.participants[0] if user_id != conversation.participants[0] else \
                conversation.participants[1]
            recipient = await self._user_repository_async.get_async(recipient_id)
            if recipient is None:
                continue
            last_message: Optional[
                Message] = await self._messages_repository_async.get_last_message_for_conversation_async(
                conversation.id
            )
            list.append(
                conversation_summaries,
                ConversationSummaryResponseDto(
                    conversation_id=conversation.id,
                    recipient_name=recipient.username,
                    last_message=last_message.text if last_message is not None else '',
                    last_message_date=conversation.updated_at or conversation.created_at
                )
            )

        return conversation_summaries

    async def get_conversation_async(self, conversation_request: ConversationRequestDto) -> \
            Optional[ConversationResponseDto]:
        conversation: Optional[Conversation] = await self._conversations_repository_async.get_user_conversation_async(
            user_id=conversation_request.user_id,
            conversation_id=conversation_request.conversation_id
        )
        if conversation is None:
            return None
        recipient_id = conversation.participants[0] if conversation_request.user_id != conversation.participants[0] \
            else conversation.participants[1]
        recipient = await self._user_repository_async.get_async(recipient_id)
        if recipient is None:
            raise Exception("Recipient not found")
        return ConversationResponseDto(
            conversation_id=conversation.id,
            recipient_name=recipient.username,
            messages=[
                MessageResponseDto(
                    text=message.text,
                    date_sent=message.created_at,
                    sender_id=message.sender_id
                )
                for message in await self._messages_repository_async.get_messages_for_conversation_async(
                    conversation_request.conversation_id
                )
            ]
        )

    async def send_message_async(self, message: SendMessageRequestDto):
        conversation: Optional[Conversation] = await self._conversations_repository_async.get_user_conversation_async(
            user_id=message.sender_id,
            conversation_id=message.conversation_id
        )
        if conversation is None:
            raise Exception("Conversation not found")

        await self._messages_repository_async.add_async(
            Message(
                conversation_id=message.conversation_id,
                sender_id=message.sender_id,
                text=message.message
            )
        )
        print(f"Sending message: {message} to conversation: {conversation.id}")
        await self._conversations_repository_async.update_async(conversation)
