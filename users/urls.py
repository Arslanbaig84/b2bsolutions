from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('', views.users, name='users'),
    path('<uid>', views.user, name='user'),
]