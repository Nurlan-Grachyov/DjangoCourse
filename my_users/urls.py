from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from .apps import UsersConfig
from .views import (
    CustomLoginView,
    ManagerUserUpdateView,
    RegisterView,
    UsersListView,
    activate, UserUpdateView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("confirm_email/<str:uidb64>/<str:token>/", activate, name="confirm_email"),
    path("list_users/", UsersListView.as_view(), name="users_list"),
    path(
        "update_users/<int:pk>/", UserUpdateView.as_view(), name="users_update"
    ),
    path(
        "manager_update_users/<int:pk>/",
        ManagerUserUpdateView.as_view(),
        name="manager_users_update",
    ),


]
