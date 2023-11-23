from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    delivery_information = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "delivery_information")


class UpdateUserForm(forms.ModelForm):
    delivery_information = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "delivery_information")
        help_texts = {
            'username': None,
        }
