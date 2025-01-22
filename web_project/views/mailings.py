from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from web_project.models import Mailing


# web_project:mailing_list- главная страница для рассылок
class MailingListView(ListView):
    model = Mailing
    template_name = "home.html"
    context_object_name = "mailings"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_mailings'] = Mailing.objects.all()
        context['active_mailings'] = Mailing.objects.all()
        return context


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing_create.html"
    fields = ["first_sending", "last_sending", "status", "message", "recipient"]
    success_url = reverse_lazy("web_project:mailing_list")


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.viewing += 1
    #     obj.save()
    #     return obj


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ["first_sending", "last_sending", "status", "message", "recipient"]
    template_name = "mailing_create.html"

    # def get_success_url(self):
    #     return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("web_project:mailing_list")
