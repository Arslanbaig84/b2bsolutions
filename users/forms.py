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
            widget= forms.CheckboxSelectMultiple(
                attrs={'class':'border-0'}
            ),
            required = True
        )

    class Meta:
        model = UserProfile
        fields = ['business_name', 'organization_type', 'business_type', 'no_of_employees', 'industry_type', 'ntn', 'contact', 'whatsapp', 'website', 'address1', 'address2', 'establishment_year']

        widgets = {
            'business_name':forms.TextInput(attrs={'class':'border-0 col-12', 'autofocus':'true'}),
            'organization_type':forms.Select(attrs={'class':'border-0 col-12'}),
            'business_type':forms.Select(attrs={'class':'border-0 col-12'}),
            'no_of_employees':forms.Select(attrs={'class':'border-0 col-12'}),
            'ntn':forms.TextInput(attrs={'class':'border-0 col-12'}),
            'contact':forms.TextInput(attrs={'class':'border-0 col-12'}),
            'whatsapp':forms.TextInput(attrs={'class':'border-0 col-12'}),
            'website':forms.URLInput(attrs={'class':'border-0 col-12'}),
            'address1':forms.TextInput(attrs={'class':'border-0 col-12'}),
            'address2':forms.TextInput(attrs={'class':'border-0 col-12'}),
            'establishment_year':forms.NumberInput(attrs={'class':'border-0 col-12'}),
        }
