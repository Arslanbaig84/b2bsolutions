from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

# Create your views here.
def product_form(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print(form)
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
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products':products})


def product(request, uid):
#    uid = uid.split(':')[1]
    product = Product.objects.get(uid = uid)
    return render(request, 'products/product.html', {'product':product})