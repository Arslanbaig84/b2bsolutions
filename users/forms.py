from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'password1' : forms.PasswordInput(),
            'password2' : forms.PasswordInput()
        }