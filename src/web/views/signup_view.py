from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject
from src.application.auth.services.signup_service_async import SignupServiceAsync
from src.application.auth.dtos.user_signup_request_dto import UserSignupRequestDto


class SignupView(MethodView):
    @inject
    def __init__(self, signup_service: SignupServiceAsync):
        self._signup_service = signup_service

    def get(self):
        return render_template("auth/signup.html")

    async def post(self):
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            return render_template("signup")
        user_dto = UserSignupRequestDto(username=username, email=email, password=password)
        await self._signup_service.signup_user(user_dto)
        return redirect(url_for("chat"))
