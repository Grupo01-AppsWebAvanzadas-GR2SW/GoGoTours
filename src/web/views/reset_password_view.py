from flask import render_template, request, redirect, url_for, session
from flask.views import MethodView
from injector import inject
from src.application.auth.services.reset_password_service_async import ResetPasswordServiceAsync
from src.application.auth.dtos.reset_password_request_dto import ResetPasswordRequestDto


class ResetPasswordView(MethodView):
    @inject
    def __init__(self, reset_password_service: ResetPasswordServiceAsync):
        self._reset_password_service = reset_password_service

    def get(self):
        if session.get("id") is not None:
            return redirect(url_for("home"))
        return render_template("auth/reset_password.html")

    async def post(self):
        reset_token = request.form.get("reset_token")
        new_password = request.form.get("new_password")

        reset_request = ResetPasswordRequestDto(reset_token=reset_token, new_password=new_password)

        success = await self._reset_password_service.reset_password(reset_token, new_password)

        if success:
            return redirect(url_for("login"))  # Redirigir al inicio de sesión después del restablecimiento
        else:
            error_msg = "Error al restablecer la contraseña. Inténtalo de nuevo."
            return render_template("auth/reset_password.html", error=error_msg)
