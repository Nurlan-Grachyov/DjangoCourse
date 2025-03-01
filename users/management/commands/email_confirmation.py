from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from config.settings import EMAIL_HOST_USER


def send_confirmation_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
    link = f"http://localhost{reverse('users:confirm_email', kwargs={'uid': uid, 'token': token})}"
    send_mail(
        'Подтвердите ваш email',
        f'Перейдите по ссылке для подтверждения: {link}',
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
