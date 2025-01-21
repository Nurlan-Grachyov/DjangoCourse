from django.contrib import admin

from web_project.models import Recipient, Message, Mailing, AttemptMailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "fullname", "comment")
    list_filter = ("fullname",)
    search_fields = ("email", "fullname")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject_letter", "body_letter")
    list_filter = ("subject_letter",)
    search_fields = ("subject_letter",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("first_sending", "last_sending", "status", "message", "recipient")
    list_filter = ("first_sending", "last_sending", "status", "recipient")
    search_fields = ("first_sending", "last_sending", "status", "recipient")


@admin.register(AttemptMailing)
class AttemptMailingAdmin(admin.ModelAdmin):
    list_display = ("date_attempt", "status", "answer", "mailing")
    list_filter = ("date_attempt", "status")
    search_fields = ("date_attempt", "status")
