from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from web_project.models import Mailing, Recipient

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_recipients"] = Recipient.objects.filter(
            owner=self.request.user
        ).count()
        context["recipients"] = Recipient.objects.filter(owner=self.request.user)
        context["count_all_mailings"] = Mailing.objects.filter(
            owner=self.request.user
        ).count()
        context["all_mailings"] = Mailing.objects.filter(owner=self.request.user)
        context["active_mailings"] = Mailing.objects.filter(
            status=Mailing.STARTED, owner=self.request.user
        )
        context["count_active_mailings"] = Mailing.objects.filter(
            status=Mailing.STARTED, owner=self.request.user
        ).count()
        return context
