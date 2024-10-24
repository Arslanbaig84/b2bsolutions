from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:product_uid>/review', views.review_form, name='review_form')
]