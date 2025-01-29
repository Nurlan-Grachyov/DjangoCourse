from django.views.generic import TemplateView

from web_project.models import Mailing, Recipient


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_recipients"] = Recipient.objects.all().count()
        context["recipients"] = Recipient.objects.all()
        context["count_all_mailings"] = Mailing.objects.all().count()
        context["all_mailings"] = Mailing.objects.all()
        context["active_mailings"] = Mailing.objects.filter(status="Запущена")
        context["count_active_mailings"] = Mailing.objects.filter(
            status="Запущена"
        ).count()
        return context
