from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render

from users.management.commands.email_confirmation import send_confirmation_email


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # send_confirmation_email(user)
        return super().form_valid(form)


def confirm_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'email_confirm_success.html')
    else:
        return render(request, 'email_confirm_failed.html')
