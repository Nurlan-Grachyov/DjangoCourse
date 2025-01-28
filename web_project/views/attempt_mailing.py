import time

from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from web_project.models import AttemptMailing, Mailing


class AttemptMailingDetailView(DetailView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_detail.html"
    context_object_name = "attempt"


class AttemptMailingCreateView(CreateView):
    model = AttemptMailing
    template_name = "attempt/create_update_attempt.html"
    fields = ["mailing"]
    # success_url = reverse_lazy("web_project:attempt_mailing_home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        return context

    def form_valid(self, form):
        try:
            mailing_id = self.request.POST.get('mailing')
            print(mailing_id)
            call_command('send_email', mailing_id=mailing_id)
            # call_command('send_email')
            mailing_instance = Mailing.objects.get(id=mailing_id)
            print(mailing_instance)
            AttemptMailing.objects.create(
                date_attempt=timezone.now(),
                status='Успешно',
                answer='Успешная отправка',
                mailing=mailing_instance
            )
            call_command('send_email')
            if not mailing_instance.status == 'Запущена':
                mailing_instance.status = 'Запущена'
                mailing_instance.save()
            # return redirect('web_project:attempt_good_create')
            return HttpResponse('Отправка была успешно создана.')
        except Exception as e:
            print(f'Ошибка: {e}')
            return HttpResponse('Произошла ошибка при отправке сообщения.')


class AttemptMailingListView(ListView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_home.html"
    context_object_name = "attempts"


class AttemptMailingUpdateView(UpdateView):
    model = AttemptMailing
    fields = ["mailing"]
    template_name = "attempt/create_update_attempt.html"


class AttemptMailingDeleteView(DeleteView):
    model = AttemptMailing
    template_name = "attempt/attempt_mailing_delete.html"
    context_object_name = "attempt"
    success_url = reverse_lazy("web_project:attempt_mailing_home")
