import logging

from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import RegisterForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .management.commands.email_confirmation import send_activation_email
# from .management.commands.email_confirmation import send_confirmation_email
from .models import CustomUser

logging.basicConfig(level=logging.DEBUG)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("my_users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        # send_activation_email(user, self.request)
        return super().form_valid(form)


class UsersListView(ListView):
    model = CustomUser
    template_name = "users_list.html"
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="managers").exists():
            context["is_in_group"] = self.request.user.groups.filter(
                name="managers"
            ).exists()
            context["all_users"] = CustomUser.objects.all()
        return context

def activate(request, uidb64, token):
    try:
        user = CustomUser.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    logging.debug(user)
    logging.debug(token)
    logging.debug(default_token_generator.check_token(user, token))
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('my_users:login')
    else:
        return HttpResponse('The confirmation link was invalid, possibly because it has already been used.')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            form.add_error(None, "Ваш аккаунт заблокирован.")
            return self.form_invalid(form)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class BlockUser(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        if not user_id:
            raise ValueError("Missing required parameter 'pk'")
        user = CustomUser.objects.get(id=user_id)

        if request.user.has_perm("my_users:can_block_user"):
            user.is_active = False
        else:
            return HttpResponseForbidden("You don't have enough rights")

        return redirect("web_project:home")
