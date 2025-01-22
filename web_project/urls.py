from django.urls import path

from web_project.apps import WebProjectConfig
from web_project.views import AttemptMailingListView, AttemptMailingCreateView, AttemptMailingDetailView, \
    AttemptMailingUpdateView, AttemptMailingDeleteView
from web_project.views.mailings import MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, \
    MailingDeleteView
from web_project.views.messages import MessageListView

from web_project.views.recipients import RecipientListView, RecipientCreateView, RecipientDetailView, \
    RecipientUpdateView, RecipientDeleteView, HomeView

app_name = WebProjectConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient_detail/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient_update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient_delete/", RecipientDeleteView.as_view(), name="recipient_delete"),

    path("message_home/", MessageListView.as_view(), name="message_home"),
    path("message_create/", RecipientCreateView.as_view(), name="message_create"),
    path("message_detail/", RecipientDetailView.as_view(), name="message_detail"),
    path("message_update/", RecipientUpdateView.as_view(), name="message_update"),
    path("message_delete/", RecipientDeleteView.as_view(), name="message_delete"),

    path("mailing_home/", MailingListView.as_view(), name="mailing_home"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing_detail/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing_update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing_delete/", MailingDeleteView.as_view(), name="mailing_delete"),

    path("attempt_mailing_home/", AttemptMailingListView.as_view(), name="attempt_mailing_home"),
    path("attempt_mailing_create/", AttemptMailingCreateView.as_view(), name="attempt_mailing_create"),
    path("attempt_mailing_detail/", AttemptMailingDetailView.as_view(), name="attempt_mailing_detail"),
    path("attempt_mailing_update/", AttemptMailingUpdateView.as_view(), name="attempt_mailing_update"),
    path("attempt_mailing_delete/", AttemptMailingDeleteView.as_view(), name="attempt_mailing_delete"),
]
