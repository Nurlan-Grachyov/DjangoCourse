import os
from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin
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
            if mailing_instance.is_Active:
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
            else:
                return render(self.request, "attempt/attempt_bad_create.html")
        except SMTPException as e:
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status=AttemptMailing.NOT_SUCCESS,
                answer=e,
                mailing=mailing_instance,
            )
            return render(self.request, "attempt/attempt_bad_create.html")


class AttemptMailingListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_home.html"
    context_object_name = "attempts"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        started_mailings = Mailing.objects.filter(status=Mailing.CREATED, owner=self.request.user)
        context['started_mailings'] = AttemptMailing.objects.filter(mailing__in=started_mailings, owner=self.request.user).count()
        context['count_attempts_mailings'] = AttemptMailing.objects.filter(owner=self.request.user).count()
        context['count_success_attempts_mailings'] = AttemptMailing.objects.filter(status=AttemptMailing.SUCCESS, owner=self.request.user).count()
        context['count_not_success_attempts_mailings'] = AttemptMailing.objects.filter(status=AttemptMailing.NOT_SUCCESS, owner=self.request.user).count()
        return context