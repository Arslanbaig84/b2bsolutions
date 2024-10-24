from django import forms
from .models import Review

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