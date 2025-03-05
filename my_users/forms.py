from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField



class BaseUserForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Input your email"}
        )
        self.fields['phone_number'].widget.attrs.update(
            {"class": "form-control", "placeholder": "You can input your phone number"}
        )


class RegisterForm(BaseUserForm, UserCreationForm):
    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].help_text = (
            "Input the same password as before for check your person"
        )
