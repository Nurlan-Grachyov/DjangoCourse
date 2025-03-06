from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from web_project.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message/message_home.html"
    context_object_name = "messages"
    success_url = reverse_lazy("web_project:message_delete")


class MessageCreateView(CreateView):
    model = Message
    template_name = "message/create_update_message.html"
    fields = ["subject_letter", "body_letter"]
    success_url = reverse_lazy("web_project:message_home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message
    template_name = "message/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject_letter", "body_letter"]
    template_name = "message/create_update_message.html"


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message/message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("web_project:message_home")
