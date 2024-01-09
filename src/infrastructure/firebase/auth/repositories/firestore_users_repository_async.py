from google.cloud.firestore import AsyncClient

from injector import inject
from src.domain.auth.entities.user import User
from src.application.auth.repositories.users_repository_async import UsersRepositoryAsync
from src.infrastructure.firebase.common.repositories.firestore_generic_repository_async import \
    FirestoreGenericRepositoryAsync
from typing import Optional
import bcrypt


class FirestoreUsersRepositoryAsync(FirestoreGenericRepositoryAsync[User, str], UsersRepositoryAsync):
    @inject
    def __init__(self, firestore_client: AsyncClient):
        super().__init__(firestore_client, 'users', User)  # nombre de la colección

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user_ref = self._firestore_client.collection('users').where('email', '==', email).limit(1)
        user_snapshot = await user_ref.get()

        for doc in user_snapshot:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            user = User(
                entity_id=doc.id,
            )

            user.merge_dict(user_data)

            return user

        return None

    async def password_matches(self, provided_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def create_user(self, user: User) -> User:
        user_data = user.to_dict()

        new_user_ref = self._firestore_client.collection('users').document()  # Firestore genera el ID
        await new_user_ref.set(user_data)

        user.entity_id = new_user_ref.id  # Actualiza el ID generado por Firestore en el objeto User
        return user

    async def update_user(self, user: User) -> Optional[User]:
        user_to_update = await self.session.query(User).filter_by(id=user.id).first()
        if user_to_update:
            user_data = user_to_update.to_dict()
            await self.session.commit()
            return user_to_update

        return None

    async def get_user_by_reset_token(self, reset_token: str) -> Optional[User]:
        user_with_token = await self.session.query(User).filter_by(reset_token=reset_token).first()
        return user_with_token