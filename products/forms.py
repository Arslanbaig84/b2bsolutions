from django import forms
from .models import Product
from users.models import Industry

class ProductForm(forms.ModelForm):

    industry = forms.ModelMultipleChoiceField(
            queryset = Industry.objects.all(),
            widget= forms.CheckboxSelectMultiple(),
            required = True
        )
    
    class Meta:
        model = Product
        fields = ['industry', 'product_name', 'product_brand', 'product_model', 'manufacturing_year', 'hours_operation', 'product_location', 'product_description', 'product_price', 'product_images']

        labels = {
            'industry':'Industry', 
            'product_name':'Product', 
            'product_brand':'Manufacturer', 
            'product_model':'Model', 
            'manufacturing_year':'Year of Production', 
            'hours_operation':'Operational Hours', 
            'product_location':'Current Location', 
            'product_description':'Product Description', 
            'product_price':'Price', 
            'product_images':'Upload Image'
        }

        widgets = {
            'product_name':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'200', 'placeholder':'Product'}), 
            'product_brand':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'200', 'placeholder':'Brand/Manufacturer'}), 
            'product_model':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'200', 'placeholder':'Product Model'}), 
            'manufacturing_year':forms.NumberInput(attrs={'class':'border-0 col-12'}), 
            'hours_operation':forms.NumberInput(attrs={'class':'border-0 col-12', 'placeholder':'Hours/Km Operation'}), 
            'product_location':forms.TextInput(attrs={'class':'border-0 col-12', 'maxlength':'200', 'placeholder':'Location'}), 
            'product_description':forms.Textarea(attrs={'class':'border-0 col-12', 'placeholder':'Description including specail features or defects'}), 
            'product_price':forms.NumberInput(attrs={'class':'border-0 col-12', 'placeholder':'Price'}), 
        }

"""    #   applying custom css to label in backend
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # add 'form-control' class to all fields
            if field_name in self.Meta.labels:
                field.widget.attrs['label'] = self.Meta.labels[field_name]"""