from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


# web_project:home - общая главная страница
from django.views.generic import TemplateView
from ..models import Recipient, Mailing


class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient/recipient_home.html"
    context_object_name = "recipients"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["count_recipients"] = Recipient.objects.all().count()
#         return context


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = "recipient/create_update_recipient.html"
    fields = ["email", "fullname", "comment"]
    success_url = reverse_lazy("web_project:recipient_home")


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipient/recipient_detail.html"
    context_object_name = "recipient"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.viewing += 1
    #     obj.save()
    #     return obj


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ["email", "fullname", "comment"]
    template_name = "recipient/create_update_recipient.html"
    success_url = reverse_lazy("web_project:recipient_home")

    # def get_success_url(self):
    #     return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient/recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("web_project:recipient_home")
