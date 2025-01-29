from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from web_project.models import Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_home.html"
    context_object_name = "mailings"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_mailings"] = Mailing.objects.all()
        context["active_mailings"] = Mailing.objects.all()
        return context


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing/create_update_mailing.html"
    fields = ["message", "recipient"]
    success_url = reverse_lazy("web_project:mailing_home")


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["first_sending", "last_sending", "status", "message", "recipient"]
    template_name = "mailing/create_update_mailing.html"
    success_url = reverse_lazy("web_project:mailing_home")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("web_project:mailing_home")
