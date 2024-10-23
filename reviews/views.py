from django.shortcuts import render
from .forms import ReviewForm
from .models import Review

# Create your views here.
def review_form(request):
    form = ReviewForm()
    return render(request, 'reviews/review.html', {'form':form})