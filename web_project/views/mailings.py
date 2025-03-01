from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
import logging
from web_project.models import Mailing, AttemptMailing
logging.basicConfig(
    level=logging.DEBUG)

class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_home.html"
    context_object_name = "mailings"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_mailings"] = Mailing.objects.all()
        context["active_mailings"] = Mailing.objects.filter(status=Mailing.STARTED)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        logging.debug('get queryset')
        active_mailings = Mailing.objects.filter(status=Mailing.STARTED)
        active_attempt_mailings = AttemptMailing.objects.filter(mailing__in=active_mailings)
        logging.debug('active_attempt_mailings')
        for attempt_mailing in active_attempt_mailings:
            if attempt_mailing.date_attempt.date() < timezone.now().date():
                mailing = attempt_mailing.mailing
                mailing.status = Mailing.ENDED
                mailing.save()
                logging.debug('update statuses for active_attempt_mailings')
                logging.debug(attempt_mailing.date_attempt.date())
                logging.debug(timezone.now().date())

        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing/create_update_mailing.html"
    fields = ["message", "recipient"]
    success_url = reverse_lazy("web_project:mailing_home")


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["message", "recipient"]
    template_name = "mailing/create_update_mailing.html"
    success_url = reverse_lazy("web_project:mailing_home")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("web_project:mailing_home")
