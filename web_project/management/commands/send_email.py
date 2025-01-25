from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        send_mail(
            "Subject here",
            "Here is the message.",
            "nurlan.grachyov@mail.com",
            ["nurlan.test_course@mail.ru"],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Email sent successfully'))