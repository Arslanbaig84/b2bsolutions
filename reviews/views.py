from django.shortcuts import render, redirect
from .forms import ReviewForm, ContactForm
from django.contrib import messages
from products.models import Product


# Create your views here.
def review_form(request, product_uid):
    product = Product.objects.get(uid = product_uid)
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.product = product
            review.save()
            messages.info(request, 'review added successfully')
            return redirect('product', uid=product.uid)
        else:
            print(form.errors)
    
    form = ReviewForm()
    return render(request, 'reviews/review.html', {'form':form, 'product':product})


def contact_us(request):
    form = ContactForm()
    return render(request, 'reviews/contact_us.html', {'form':form})