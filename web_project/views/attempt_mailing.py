from django.core.management import call_command
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pyexpat.errors import messages
from django.contrib import messages

from web_project.models import AttemptMailing, Mailing


class AttemptMailingListView(ListView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_home.html"
    context_object_name = "attempts"


class AttemptMailingCreateView(CreateView):
    model = AttemptMailing
    template_name = "attempt/create_update_attempt.html"
    fields = ["mailing"]
    success_url = reverse_lazy("web_project:attempt_mailing_home")

    def form_valid(self, form):
        try:
            call_command('send_email')
            messages.success(self.request, "Email sent successfully")
            # self.request.session['success_status'] = 'success'
            mailing_id = self.kwargs.get('mailing_id')
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status='успешно',
                answer='Успешная отправка',
                mailing=
            )
        except Exception as e:
            messages.error(self.request, f"Email sent failed: {e}")
            # self.request.session['success_status'] = 'failed'
            # self.request.session['answer'] = f'{e}'
            mailing_id = self.kwargs.get('mailing_id')
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status='успешно',
                answer='Успешная отправка',
                mailing=
            )
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['status'] = self.request.session.pop('success_status', 'unknown')
    #     context['answer'] = self.request.session.pop('answer', 'Good')
    #     return context


class AttemptMailingDetailView(DetailView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_detail.html"
    context_object_name = "attempt"


class AttemptMailingUpdateView(UpdateView):
    model = AttemptMailing
    fields = ["mailing"]
    template_name = "attempt/create_update_attempt.html"


class AttemptMailingDeleteView(DeleteView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_delete.html"
    context_object_name = "attempt"
    success_url = reverse_lazy("web_project:attempt_mailing_home")
