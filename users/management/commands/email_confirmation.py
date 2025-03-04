import logging

from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator

from config.settings import EMAIL_HOST_USER

logging.basicConfig(
    level=logging.DEBUG)


def send_confirmation_email(user):
    token = default_token_generator.make_token(user)
    logging.debug(token)
    logging.debug(user)
    logging.debug(default_token_generator.check_token(user, token))
    link = f"http://localhost:8000{reverse('users:confirm_email', kwargs={'uidb64': user.pk, 'token': token})}"
    logging.debug('link good')
    send_mail(
        'Подтвердите ваш email',
        f'Перейдите по ссылке для подтверждения: {link}',
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    logging.debug('send good')
