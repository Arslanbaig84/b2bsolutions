from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product_form', views.product_form, name='product_form')
]