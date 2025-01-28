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

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        mailing_instance = AttemptMailing.objects.creatget(mailing_id=mailing_id)
        try:
            send_mail(
                mailing_instance.message.subject_letter,
                mailing_instance.message.body_letter,
                # 'TEST',
                # 'test',
                os.getenv('EMAIL_HOST_USER'),
                ["nurlan.test_course@mail.ru"],
                fail_silently=False,
            )
            self.stdout.write('Email sent successfully')
        except Exception as e:
            self.stdout.write(f'Failed to send email: {e}')
