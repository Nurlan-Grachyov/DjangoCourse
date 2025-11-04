import logging

from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.views import (
    LoginView,
    PasswordContextMixin,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from config import settings

from .forms import ManagerUserForm, OwnerUserForm, RegisterForm
from .management.commands.email_confirmation import send_activation_link
from .models import CustomUser

logging.basicConfig(
    filename="logging.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='Utf-8',
)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("my_users:login")

    def form_valid(self, form):
        user = form.save()
        send_activation_link(user)
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = OwnerUserForm
    template_name = "crud/update_user.html"
    success_url = reverse_lazy("web_project:mailing_home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.request.user.pk
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
    if user is not None and token == user.token:
        group_users = Group.objects.get(name="users")
        user.groups.add(group_users)
        user.is_staff = True
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


class PasswordResetViewMy(PasswordResetView, PasswordContextMixin, FormView):
    success_url = reverse_lazy("my_users:password_reset_done")

    def get_success_url(self):
        return self.success_url

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            logging.error(f"Ошибка при сбросе пароля: {e}")
            return HttpResponse("Sorry, there was a mistake, try later", status=500)


class PasswordResetConfirmViewMy(
    PasswordResetConfirmView, PasswordContextMixin, FormView
):
    success_url = reverse_lazy("my_users:password_reset_complete")

    def get_success_url(self):
        return self.success_url

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            logging.error(f"Ошибка при сбросе пароля: {e}")
            return HttpResponse("Sorry, there was a mistake, try later", status=500)


class PasswordResetCompleteViewMy(
    PasswordResetCompleteView, PasswordContextMixin, TemplateView
):

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["login_url"] = resolve_url(f"my_users:{settings.LOGIN_URL}")
            return context
        except Exception as e:
            logging.error(f"Ошибка при сбросе пароля: {e}")
            return HttpResponse("Sorry, there was a mistake, try later")
