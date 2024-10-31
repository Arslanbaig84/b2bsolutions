from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from reviews.models import Review

# Create your views here.
def product_form(request):
    user = request.user
#    print(user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
#        print(form)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = user
            product.save()
            return redirect('products')
        else:
            print(form.errors)

    form = ProductForm()
    return render(request, 'products/product_form.html', {'form':form})


def products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/products.html', {'products':products})


def product(request, uid):
#    uid = uid.split(':')[1]
    product = Product.objects.get(uid = uid)
    reviews = Review.objects.filter(product=product)
    for review in reviews:
        print(review.review)
    return render(request, 'products/product.html', {'product':product, 'reviews':reviews})