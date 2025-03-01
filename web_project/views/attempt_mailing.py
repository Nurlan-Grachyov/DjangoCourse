import os
from smtplib import SMTPException
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import (
    CreateView,
    ListView,
)

from web_project.models import AttemptMailing, Mailing


class AttemptMailingCreateView(CreateView):
    model = AttemptMailing
    template_name = "attempt/create_update_attempt.html"
    fields = ["mailing"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailings"] = Mailing.objects.all()
        return context

    def form_valid(self, form):
        """Send a main email"""
        mailing_id = self.request.POST.get("mailing")
        mailing_instance = Mailing.objects.get(id=mailing_id)
        try:
            send_mail(
                mailing_instance.message.subject_letter,
                mailing_instance.message.body_letter,
                os.getenv("EMAIL_HOST_USER"),
                ["nurlan.test_course@mail.ru"],
                fail_silently=False,
            )
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status=AttemptMailing.SUCCESS,
                answer="success sending",
                mailing=mailing_instance,
            )
            if not mailing_instance.status == Mailing.STARTED:
                mailing_instance.status = Mailing.STARTED
                mailing_instance.save()
            return render(self.request, "attempt/attempt_good_create.html")
        except SMTPException as e:
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status=AttemptMailing.NOT_SUCCESS,
                answer=e,
                mailing=mailing_instance,
            )
            return render(self.request, "attempt/attempt_bad_create.html")


class AttemptMailingListView(ListView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_home.html"
    context_object_name = "attempts"
