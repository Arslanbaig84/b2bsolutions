from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_form, name='review_form')
]