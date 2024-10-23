from django import forms
from .models import Review
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label= 'Rating',
        choices = [
        ('', 'Select a rating'),  # Empty default option
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.Select,
        required=True
    )

    class Meta:
        model = Review
        fields = ['rating', 'review']