import os

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from web_project.models import AttemptMailing

load_dotenv()


class Command(BaseCommand):
    help = "Send a test email"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID of the mailing")

    def handle(self, *args, **kwargs):
        mailing_id = kwargs["mailing_id"]
        attempt_mailing = (
            AttemptMailing.objects.filter(mailing_id=mailing_id)
            .order_by("-date_attempt")
            .first()
        )
        try:
            send_mail(
                attempt_mailing.mailing.message.subject_letter,
                attempt_mailing.mailing.message.body_letter,
                os.getenv("EMAIL_HOST_USER"),
                ["nurlan.test_course@mail.ru"],
                fail_silently=False,
            )
            self.stdout.write("Email sent successfully")
        except Exception as e:
            self.stdout.write(f"Failed to send email: {e}")
