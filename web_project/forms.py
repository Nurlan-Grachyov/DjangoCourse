import logging

from django import forms
from .models import Mailing, Message, Recipient

logging.basicConfig(level=logging.DEBUG)


class OwnerMailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["recipient"].queryset = Recipient.objects.filter(owner=user)
        self.fields["message"].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Mailing
        fields = ["message", "recipient"]


class ManagerMailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["is_active"]
