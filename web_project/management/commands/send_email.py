import os

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from dotenv import load_dotenv
from web_project.models import Mailing, AttemptMailing

load_dotenv()


class Command(BaseCommand):
    help = 'Send a test email'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID of the mailing')
        print(parser)

    def handle(self, *args, **kwargs):
        print(parser)
        mailing_id = kwargs['mailing_id']
        print(mailing_id)
        attempt_mailing = AttemptMailing.objects.filter(mailing_id=mailing_id).order_by('-date_attempt').first()
        if attempt_mailing is None:
            print("No records found")
        try:
            # print(attempt_mailing.mailing_id.message.subject_letter)
            # print(attempt_mailing)
            send_mail(
                attempt_mailing.mailing.message.subject_letter,
                attempt_mailing.mailing.message.body_letter,
                # 'TEST',
                # 'test',
                os.getenv('EMAIL_HOST_USER'),
                ["nurlan.test_course@mail.ru"],
                fail_silently=False,
            )
            self.stdout.write('Email sent successfully')
        except Exception as e:

            self.stdout.write(f'Failed to send email: {e}')
