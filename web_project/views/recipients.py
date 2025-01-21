from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from web_project.models import Recipient

# web_project:home - общая главная страница

class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(is_created=True)


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = "recipient_create.html"
    fields = ["email", "fullname", "comment"]
    success_url = reverse_lazy("web_project:home")


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.viewing += 1
    #     obj.save()
    #     return obj


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ["email", "fullname", "comment"]
    template_name = "recipient_create.html"

    # def get_success_url(self):
    #     return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("web_project:home")
