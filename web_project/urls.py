from django.urls import path

from web_project.apps import WebProjectConfig
from web_project.views import (
    AttemptMailingCreateView,
    AttemptMailingListView,
)
from web_project.views.home_page import HomeView
from web_project.views.mailings import (
    MailingCreateView,
    MailingDeleteView,
    MailingListView,
    MailingUpdateView,
)
from web_project.views.messages import (
    MessageCreateView,
    MessageDeleteView,
    MessageListView,
    MessageUpdateView,
)
from web_project.views.recipients import (
    RecipientCreateView,
    RecipientDeleteView,
    RecipientListView,
    RecipientUpdateView,
)

app_name = WebProjectConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipient_home/", RecipientListView.as_view(), name="recipient_home"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient_update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient_delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("message_home/", MessageListView.as_view(), name="message_home"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailing_home/", MailingListView.as_view(), name="mailing_home"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing_update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path(
        "attempt_mailing_home/",
        AttemptMailingListView.as_view(),
        name="attempt_mailing_home",
    ),
    path(
        "attempt_mailing_create/",
        AttemptMailingCreateView.as_view(),
        name="attempt_mailing_create",
    ),
]
