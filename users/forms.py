from .models import CustomUser, UserProfile, Industry
from django import forms
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.core.exceptions import ValidationError
import re


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

        help_texts = {
            'ntn':'NTN must follow format 1234567-8',
            'establishment_year':'Year must be between 1900 and current year.'
        }

        labels = {
            'business_name':'Business Name', 
            'organization_type':'Organization Type', 
            'business_type':'Business Type', 
            'no_of_employees':'No of Employees', 
            'industry_type':'Industry Type', 
            'ntn':'NTN', 
            'contact':'Contact', 
            'whatsapp':'Whatsapp', 
            'website':'Website URL', 
            'address1':'Address1', 
            'address2':'Address2', 
            'establishment_year':'Year of Establishment'
        }

        widgets = {
            'business_name':forms.TextInput(attrs={'class':'border-0 col-12', 'autofocus':'true', 'maxlength':'200', 'placeholder':'Business Name'}),
            'organization_type':forms.Select(attrs={'class':'border-0 col-12'}),
            'business_type':forms.Select(attrs={'class':'border-0 col-12'}),
            'no_of_employees':forms.Select(attrs={'class':'border-0 col-12'}),
            'ntn':forms.TextInput(attrs={'class':'border-0 col-12', 'pattern': r'^\d{7}-\d{1}$', 'title': "Format: '1234567-8'"}),
            'contact':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'20', 'placeholder':'Contact'}),
            'whatsapp':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'20', 'placeholder':'Whatsapp'}),
            'website':forms.URLInput(attrs={'class':'border-0 col-12', 'placeholder':'Website URL'}),
            'address1':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'200', 'placeholder':'Primary Address'}),
            'address2':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'200', 'placeholder':'Secondary Address'}),
            'establishment_year':forms.NumberInput(attrs={'class':'border-0 col-12',
                                                          'min':'1900',
                                                          'max':datetime.date.today().year}),
                                                          'title':'Enter a year between 1900 and current year'
        }

        error_messages = {
            'ntn': {
                'invalid': "NTN must follow the format '1234567-8'.",
                'unique': "This NTN is already in use.",
            }
        }
    
    def clean_ntn(self):
        ntn = self.cleaned_data.get('ntn')

        # Step 1: Format Validation with Regex
        if ntn:
            ntn_pattern = r'^\d{7}-\d{1}$'
            if not re.match(ntn_pattern, ntn):
                raise ValidationError("NTN must follow the format '1234567-8'.")

        # Step 2: Uniqueness Check
        if ntn:
            qs = UserProfile.objects.filter(ntn=ntn)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("This NTN is already in use.")

        # Step 3: Additional Validation (e.g., disallowed values)
        if ntn and ntn.startswith('0000000'):
            raise ValidationError("NTN cannot start with '0000000'.")

        return ntn

    def clean_establishment_year(self):
        year = self.cleaned_data.get('establishment_year')
        if year:
            if year < 1900 or year > datetime.date.today().year:
                raise ValidationError("Year must be between 1900 and the current year.")
        return year


    
