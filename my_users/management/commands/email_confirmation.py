import logging

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from config.settings import EMAIL_HOST_USER

logging.basicConfig(level=logging.DEBUG)


def send_activation_link(user, request):
    token = default_token_generator.make_token(user)
    uid = user.pk
    logging.debug(user)
    logging.debug(token)
    logging.debug(default_token_generator.check_token(user, token))
    user.token = token
    activation_link = f"http://localhost:8000{reverse('my_users:confirm_email', kwargs={'uidb64': uid,
                                                                                        'token': token})}"
    subject = "Активируйте ваш аккаунт"
    message = render_to_string(
        "activation.txt", {"user": user, "activation_link": activation_link}
    )
    send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=False)
    logging.debug(user)
    logging.debug(token)
    logging.debug(default_token_generator.check_token(user, token))
