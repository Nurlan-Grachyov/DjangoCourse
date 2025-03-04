import logging

from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from config.settings import EMAIL_HOST_USER
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


# class PasswordResetViewMy(FormView):
#     form_class = PasswordResetForm
#     template_name = "registration/password_reset_form.html"
#     success_url = reverse_lazy('users:password_reset_done')
#     from_email = None
#     token_generator = default_token_generator
#
#     def form_valid(self, form):
#         logging.debug('good')
#         user = form.save()
#         logging.debug(user)
#         link = f"http://localhost:8000{reverse('users:password_reset_done', kwargs={'uidb64': user.pk, 'token': self.token_generator})}"
#         send_mail(
#             'Смена пароля',
#             f'Перейдите по ссылке для подтверждения: {link}',
#             EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False,
#         )
