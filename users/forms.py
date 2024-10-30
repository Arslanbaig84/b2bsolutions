from .models import CustomUser, UserProfile, Industry
from django import forms
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.core.exceptions import ValidationError
import re

current_year = datetime.date.today().year

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
                                                          'max':current_year}),
                                                          'title':'Enter a year between 1900 and current year'
        }

        error_messages = {
            'ntn': {
                'invalid': "NTN must follow the format '1234567-8'.",
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

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            qs = UserProfile.objects.filter(contact=contact)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Contact no already in use.")
        return contact

    def clean_establishment_year(self):
        year = self.cleaned_data.get('establishment_year')
        if year >= 1900 and year <= current_year:
            return year
        else:
            raise ValidationError("Year should be between 1900 and current year")
        
    def clean_organization_type(self):
        organization_type = self.cleaned_data.get('organization_type')

        # Access the valid choices directly from the field
        valid_choices = dict(self._meta.model._meta.get_field('organization_type').choices)

        # Check if the submitted value is in the valid choices
        if organization_type not in valid_choices:
            raise forms.ValidationError(f"{organization_type} is not a valid choice.")

        return organization_type

    def clean_business_type(self):
        business_type = self.cleaned_data.get('business_type')
        valid_choices = dict(self._meta.model._meta.get_field('business_type').choices)
        if business_type not in valid_choices:
            raise forms.ValidationError(f'{business_type} is an INVALID CHOICE')
        return business_type
        
    def clean_no_of_employees(self):
        employees = self.cleaned_data.get('no_of_employees')
        valid_choices = dict(self._meta.model._meta.get_field('no_of_employees').choices)
        if employees not in valid_choices:
            raise forms.ValidationError(f'{employees} is an INVALID CHOICE')
        return employees
    
    def clean_industry_type(self):
        industries = list(self.cleaned_data.get('industry_type'))
        if not industries:
            raise forms.ValidationError(f'You must select at least one Industry')
        valid_choices = list(Industry.objects.values_list('id', flat=True))
        for industry in industries:
            if industry.id not in valid_choices:
                raise forms.ValidationError(f'{industry} is an INVALID CHOICE')
        return industries