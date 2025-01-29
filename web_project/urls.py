from django.urls import path

from web_project.apps import WebProjectConfig
from web_project.views import (
    AttemptMailingCreateView,
    AttemptMailingDeleteView,
    AttemptMailingDetailView,
    AttemptMailingListView,
    AttemptMailingUpdateView, AttemptMailingTemplateView,
)
from web_project.views.home_page import HomeView
from web_project.views.mailings import (
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingUpdateView,
)
from web_project.views.messages import (
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
)
from web_project.views.recipients import (
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientListView,
    RecipientUpdateView,
)

app_name = WebProjectConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipient_home/", RecipientListView.as_view(), name="recipient_home"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient_detail/<int:pk>/",
        RecipientDetailView.as_view(),
        name="recipient_detail",
    ),
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
        "message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"
    ),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("mailing_home/", MailingListView.as_view(), name="mailing_home"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing_detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"
    ),
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
    path(
        "attempt_mailing_detail/<int:pk>/",
        AttemptMailingDetailView.as_view(),
        name="attempt_mailing_detail",
    ),
    path(
        "attempt_mailing_update/<int:pk>/",
        AttemptMailingUpdateView.as_view(),
        name="attempt_mailing_update",
    ),
    path(
        "attempt_mailing_delete/<int:pk>/",
        AttemptMailingDeleteView.as_view(),
        name="attempt_mailing_delete",
    ),
    path(
        "attempt_bad_create/",
        AttemptMailingTemplateView.as_view(),
        name="attempt_bad_create",
    ),
]
