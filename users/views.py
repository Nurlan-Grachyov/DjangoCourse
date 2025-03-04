import logging

from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render

from users.management.commands.email_confirmation import send_confirmation_email

logging.basicConfig(
    level=logging.DEBUG)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        # send_confirmation_email(user)
        return super().form_valid(form)


def confirm_email(request, uidb64, token):
    User = get_user_model()
    logging.debug('confirm_email')
    try:
        user = User.objects.get(pk=uidb64)
        logging.debug('get user')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logging.debug('user none')
        user = None
    logging.debug(token)
    logging.debug(user)
    logging.debug(default_token_generator.check_token(user, token))
    if user is not None and default_token_generator.check_token(user, token):
        logging.debug('USER TRUE!!!')
        user.is_active = True
        user.save()
        return render(request, 'result_confirm_email/email_confirm_success.html')
    else:
        logging.debug('user bad!!!')
        return render(request, 'result_confirm_email/email_confirm_failed.html')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            form.add_error(None, "Ваш аккаунт заблокирован.")
            return self.form_invalid(form)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
