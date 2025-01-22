from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from web_project.models import AttemptMailing

# web_project:attempt_mailing_list - главная страница для попыток
class AttemptMailingListView(ListView):
    model = AttemptMailing
    template_name = "attempt_mailing_list.html"
    context_object_name = "attempts"

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(is_created=True)


class AttemptMailingCreateView(CreateView):
    model = AttemptMailing
    template_name = "attempt_mailing_create.html"
    fields = ["date_attempt", "status", "answer", "mailing"]
    success_url = reverse_lazy("web_project:attempt_mailing_list")


class AttemptMailingDetailView(DetailView):
    model = AttemptMailing
    template_name = "attempt_mailing_detail.html"
    context_object_name = "attempt"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     obj.viewing += 1
    #     obj.save()
    #     return obj


class AttemptMailingUpdateView(UpdateView):
    model = AttemptMailing
    fields = ["date_attempt", "status", "answer", "mailing"]
    template_name = "attempt_mailing_create.html"

    # def get_success_url(self):
    #     return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class AttemptMailingDeleteView(DeleteView):
    model = AttemptMailing
    template_name = "attempt_mailing_delete.html"
    context_object_name = "attempt"
    success_url = reverse_lazy("web_project:attempt_mailing_list")
