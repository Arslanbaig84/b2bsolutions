from .models import CustomUser, UserProfile, Industry
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

class UserProfileForm(forms.ModelForm):
    
    industry_type = forms.ModelMultipleChoiceField(
            queryset = Industry.objects.all(),
            widget= forms.CheckboxSelectMultiple,
            required = True
        )

    class Meta:
        model = UserProfile
        fields = ['business_name', 'organization_type', 'business_type', 'no_of_employees', 'industry_type', 'ntn', 'contact', 'whatsapp', 'website', 'address1', 'address2', 'establishment_year']
