from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from injector import inject
from src.application.auth.services.login_service_async import LoginServiceAsync
from src.application.auth.dtos.user_login_request_dto import UserLoginRequestDto
from flask import session

class LoginView(MethodView):
    @inject
    def __init__(self, login_service: LoginServiceAsync):
        self._login_service = login_service

    def get(self):
        return render_template("auth/login.html")

    async def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        user_dto = UserLoginRequestDto(email=email, password=password)
        logged_user = await self._login_service.login(user_dto)

        if logged_user:
            print("aun no falla")
            session["id"] = logged_user.id
            print("id= " + str(session["id"]))
            session['is_admin'] = logged_user.is_admin
            print(f"id= {bool(str(session['is_admin']))}")
            return redirect(url_for("home"))  # Redirigir a chat si el inicio es exitoso
        else:
            error_msg = "Inicio de sesión fallido. Inténtalo de nuevo."
            return render_template("auth/login.html", error=error_msg)