from django import forms
from .models import Review, Contact

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        label= 'Rating',
        min_value=1,
        max_value=5,
        widget = forms.Select(choices=[
        ('', 'Select a rating'),  # Empty default option
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]),
        required=True
    )

    class Meta:
        model = Review
        fields = ['rating', 'review']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['text']

        labels = {'text':'Suggestion'}

        widgets = {
            'text':forms.Textarea(attrs={'class':'col-12 border border-1 border-primary', 'placeholder':'We would love to hear your suggestions.'})
        }