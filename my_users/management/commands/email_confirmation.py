import logging
from smtplib import SMTPException

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

from config.settings import EMAIL_HOST_USER

logging.basicConfig(
    filename="logging.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='Utf-8',
)


def send_activation_link(user):
    token = default_token_generator.make_token(user)
    uid = user.pk

    user.token = token
    try:
        activation_link = f"http://localhost:8000{reverse('my_users:confirm_email', kwargs={'uidb64': uid, 'token': token})}"
    except Exception as e:
        logging.error(f"Ошибка при генерации ссылки подтверждения: {e}")
        return HttpResponse(
            "The confirmation link was invalid, possibly because it has already been used."
        )
    subject = "Активируйте ваш аккаунт"
    message = render_to_string(
        "activation.txt", {"user": user, "activation_link": activation_link}
    )
    try:
        send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=False)
    except SMTPException as e:
        logging.warning(f"Ошибка при отправке ссылке подтверждения: {e}")
