from django import forms
from .models import Product
from users.models import Industry

class ProductForm(forms.ModelForm):
    industry = forms.ModelMultipleChoiceField(
            queryset = Industry.objects.all(),
            widget= forms.CheckboxSelectMultiple,
            required = True
        )

    class Meta:
        model = Product
        fields = ['industry', 'product_name', 'product_model', 'manufacturing_year', 'hours_operation', 'product_location', 'product_description', 'product_price', 'product_images']