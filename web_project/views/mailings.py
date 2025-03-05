from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
import logging

from web_project.forms import MailingForm
from web_project.models import Mailing, AttemptMailing

logging.basicConfig(
    level=logging.DEBUG)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["all_mailings"] = Mailing.objects.filter(owner=self.request.user).count()
            context["created_mailings"] = Mailing.objects.filter(status=Mailing.CREATED, owner=self.request.user).count()
            context["active_mailings"] = Mailing.objects.filter(status=Mailing.STARTED, owner=self.request.user).count()
            context["ended_mailings"] = Mailing.objects.filter(status=Mailing.ENDED, owner=self.request.user).count()
        else:
            return context
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        active_mailings = Mailing.objects.filter(status=Mailing.STARTED)
        active_attempt_mailings = AttemptMailing.objects.filter(mailing__in=active_mailings)
        for attempt_mailing in active_attempt_mailings:
            if attempt_mailing.date_attempt.date() < timezone.now().date():
                mailing = attempt_mailing.mailing
                mailing.status = Mailing.ENDED
                mailing.save()

        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing/create_update_mailing.html"
    form_class = MailingForm
    success_url = reverse_lazy("web_project:mailing_home")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/create_update_mailing.html"
    success_url = reverse_lazy("web_project:mailing_home")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("web_project:mailing_home")
