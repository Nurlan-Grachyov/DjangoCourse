from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..models import Message, Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipient/recipient_home.html"
    context_object_name = "recipients"


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = "recipient/create_update_recipient.html"
    fields = ["email", "fullname", "comment"]
    success_url = reverse_lazy("web_project:recipient_home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ["email", "fullname", "comment"]
    template_name = "recipient/create_update_recipient.html"
    success_url = reverse_lazy("web_project:recipient_home")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient/recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("web_project:recipient_home")
