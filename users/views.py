from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import CustomUser
from .tokens import account_activation_token
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Create user with your custom manager
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                # Any additional fields from form.cleaned_data can go here
            )
            messages.success(request, 'User created, please check email for verification.')
            return redirect('/')  # Redirect after successful registration
    else:
        form = CustomUserForm()
    
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('register')
    else:
        messages.info(request, 'Please activate your account by visiting your email(Remember to check spam).')
        return redirect('/')
    

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login Successful.')
            return redirect('/')
        else:
            messages(request, 'Invalid username or password')
            return redirect('login_user')
    
    return render(request, 'users/login_user.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('/')

INDUSTRIES = [
    ('aerospace', 'Aerospace'),
    ('agriculture', 'Agriculture'),
    ('apparel/textile', 'Apparel/Textile'),
    ('automotive', 'Automotive'),
    ('banking', 'Banking'),
    ('chemical_manufacturing', 'Chemical_Manufacturing'),
    ('construction/contrating', 'Construction/Contrating'),
    ('consulting', 'Consulting'),
    ('consumer_goods', 'Consumer_Goods'),
    ('defence', 'Defence'),
    ('e_commerce', 'E_Commerce'),
    ('education', 'Education'),
    ('energy/oil_gas', 'Energy/Oil_Gas'),
    ('engineering', 'Engineering'),
    ('entertainment', 'Entertainment'),
    ('event_management', 'Event_Management'),
    ('food_beverages', 'Food_Beverages'),
    ('govt/utilties', 'Govt/Utilities'),
    ('healthcare/pharma', 'Healthcare/Pharma'),
    ('heavy_equipment', 'Heavy_Equipment'),
    ('it/software/ai', 'IT/Software/AI'),
    ('journalism', 'Journalism'),
    ('legal_services', 'Legal_Services'),
    ('logistic', 'Logistic'),
    ('mining', 'Mining'),
    ('real_estate', 'Real_Estate'),
    ('retail', 'Retail'),
    ('sports', 'Sports'),
    ('telecom', 'Telecom'),
    ('tourism', 'Tourism'),
    ('other', 'Other')
              ]
