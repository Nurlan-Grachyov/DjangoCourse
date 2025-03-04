from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from users.apps import UsersConfig
from users.views import RegisterView, confirm_email, CustomLoginView, PasswordResetViewMy

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("confirm_email/<str:uidb64>/<str:token>/", confirm_email, name='confirm_email'),
    path("password-reset/", PasswordResetViewMy.as_view(), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r"^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$",
            auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
