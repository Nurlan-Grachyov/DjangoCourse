from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, confirm_email, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("confirm_email/<str:uidb64>/<str:token>/", confirm_email, name='confirm_email'),
path(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
path(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
path(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

]
