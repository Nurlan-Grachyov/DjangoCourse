import logging

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordContextMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView

from .forms import ManagerUserForm, OwnerUserForm, RegisterForm
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


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = OwnerUserForm
    template_name = "crud/update_user.html"
    success_url = reverse_lazy("web_project:mailing_home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.pk)
        context['pk'] = self.request.user.pk
        return context


class ManagerUserUpdateView(UpdateView):
    model = CustomUser
    template_name = "crud/manager_update_user.html"
    success_url = reverse_lazy("web_project:mailing_home")

    def get_form_class(self):
        user = self.request.user
        logging.debug(user)
        if user.groups.filter(name="managers").exists():
            logging.debug("ManagerUserForm")
            return ManagerUserForm
        elif user == self.object.owner:
            logging.debug("OwnerUserForm")
            return OwnerUserForm
        raise PermissionDenied


class UsersListView(ListView):
    model = CustomUser
    template_name = "crud/users_list.html"
    context_object_name = "users"

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
        return redirect("my_users:login")
    else:
        return HttpResponse(
            "The confirmation link was invalid, possibly because it has already been used."
        )


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            form.add_error(None, "Ваш аккаунт заблокирован.")
            return self.form_invalid(form)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class PasswordResetView(PasswordContextMixin, FormView):
    success_url = reverse_lazy('my_users:password_reset_done')
