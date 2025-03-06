from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .apps import UsersConfig
from .views import RegisterView, confirm_email, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "confirm_email/<str:uidb64>/<str:token>/", confirm_email, name="confirm_email"
    ),
]
