from abc import ABC, abstractmethod
from src.application.auth.dtos.user_login_request_dto import UserLoginRequestDto
from src.application.auth.dtos.user_signup_request_dto import UserSignupRequestDto
from src.application.auth.dtos.user_response_dto import UserResponseDto
from src.application.auth.dtos.reset_password_request_dto import ResetPasswordRequestDto

class ResetPasswordServiceAsync(ABC):
    @abstractmethod
    async def request_reset_password(self, reset_request: ResetPasswordRequestDto) -> None:
        """
        Envía un correo electrónico o mensaje para solicitar el restablecimiento de la contraseña.
        """
        pass

    @abstractmethod
    async def reset_password(self, reset_token: str, new_password: str) -> bool:
        """
        Restablece la contraseña del usuario utilizando un token de reinicio y la nueva contraseña.
        Retorna un booleano indicando si el restablecimiento fue exitoso.
        """
        pass