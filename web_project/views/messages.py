from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from web_project.models import Message

# web_project:message_list - главная страница для сообщений

class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(is_created=True)


class MessageCreateView(CreateView):
    model = Message
    template_name = "message_create.html"
    fields = ["subject_letter", "body_letter"]
    success_url = reverse_lazy("web_project:message_list")


class MessageDetailView(DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.viewing += 1
    #     obj.save()
    #     return obj


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject_letter", "body_letter"]
    template_name = "message_create.html"

    # def get_success_url(self):
    #     return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("web_project:message_list")
