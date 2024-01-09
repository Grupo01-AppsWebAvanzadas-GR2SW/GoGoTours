from abc import ABC
from application.auth.dtos.reset_password_request_dto import ResetPasswordRequestDto
from application.auth.services.reset_password_service_async import ResetPasswordServiceAsync
from src.domain.auth.entities.user import User
from src.application.auth.services.login_service_async import LoginServiceAsync
from src.application.auth.dtos.user_login_request_dto import UserLoginRequestDto
from src.application.auth.dtos.user_response_dto import UserResponseDto
from src.application.auth.repositories.users_repository_async import UsersRepositoryAsync
from injector import inject
from typing import Optional

import bcrypt
import string
import secrets


def generate_reset_token(self, length=24):
    alphabet = string.ascii_letters + string.digits
    reset_token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return reset_token


class DefaultResetPasswordServiceAsync(ResetPasswordServiceAsync):
    @inject
    def __init__(self, users_repository_async: UsersRepositoryAsync):
        self._users_repository_async = users_repository_async

    async def request_reset_password(self, reset_request: ResetPasswordRequestDto) -> None:
        user = await self._users_repository_async.get_user_by_email(reset_request.email)
        if user:
            reset_token = generate_reset_token()

            user.reset_token = reset_token
            await self._users_repository_async.update_user(user)

    async def reset_password(self, reset_token: str, new_password: str) -> bool:
        user = await self._users_repository_async.get_user_by_reset_token(reset_token)
        if user:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = hashed_password
            user.reset_token = None
            await self._users_repository_async.update_user(user)
            return True
        return False
