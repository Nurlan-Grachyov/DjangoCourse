from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
import logging

from web_project.forms import OwnerMailingForm, ManagerMailingForm
from web_project.models import Mailing, AttemptMailing

logging.basicConfig(level=logging.DEBUG)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="managers").exists():
            context["is_in_group"] = self.request.user.groups.filter(
                name="managers"
            ).exists()
            context["all_mailings"] = (
                Mailing.objects.all().count()
                if Mailing.objects.all().count() > 0
                else 0
            )
            context["created_mailings"] = (
                Mailing.objects.filter(status=Mailing.CREATED).count()
                if Mailing.objects.filter().count() > 0
                else 0
            )
            context["active_mailings"] = (
                Mailing.objects.filter(status=Mailing.STARTED).count()
                if Mailing.objects.filter().count() > 0
                else 0
            )
            context["ended_mailings"] = (
                Mailing.objects.filter(status=Mailing.ENDED).count()
                if Mailing.objects.filter().count() > 0
                else 0
            )

        elif user.groups.filter(name="users").exists():
            context["all_mailings"] = (
                Mailing.objects.filter(owner=user).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
            logging.debug(context["all_mailings"])
            context["created_mailings"] = (
                Mailing.objects.filter(owner=user, status=Mailing.CREATED).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
            context["active_mailings"] = (
                Mailing.objects.filter(owner=user, status=Mailing.STARTED).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
            context["ended_mailings"] = (
                Mailing.objects.filter(owner=user, status=Mailing.ENDED).count()
                if Mailing.objects.filter(owner=user).count() > 0
                else 0
            )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        active_mailings = Mailing.objects.filter(status=Mailing.STARTED)
        active_attempt_mailings = AttemptMailing.objects.filter(
            mailing__in=active_mailings
        )
        for attempt_mailing in active_attempt_mailings:
            if attempt_mailing.date_attempt.date() < timezone.now().date():
                mailing = attempt_mailing.mailing
                mailing.status = Mailing.ENDED
                mailing.save()

        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing/create_update_mailing.html"
    form_class = OwnerMailingForm
    success_url = reverse_lazy("web_project:mailing_home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = "mailing/create_update_mailing.html"
    success_url = reverse_lazy("web_project:mailing_home")

    def get_form_class(self):
        user = self.request.user
        logging.debug(user)
        if user == self.object.owner:
            logging.debug("OwnerMailingForm")
            return OwnerMailingForm
        elif user.has_perm("web_project:can_disabling_mailings"):
            logging.debug("ManagerMailingForm")
            return ManagerMailingForm
        raise PermissionDenied


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("web_project:mailing_home")
