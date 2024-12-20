from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import CustomUser, UserProfile, Industry
from .tokens import account_activation_token
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q


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
            messages.warning(request, 'Invalid username or password')
            return redirect('login_user')
    
    return render(request, 'users/login_user.html')


@login_required(login_url="/users/login_user/")
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('/')


@login_required(login_url="/users/login_user/")
def userprofile(request):
    profile = request.user.profile
    return render(request, 'users/userprofile.html', {'profile':profile})


@login_required(login_url="/users/login_user/")
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
#        contact = request.POST.get('contact')
#        ToDO implementation of same contact exclusion of current user
#        if UserProfile.objects.filter(contact=contact):
#            messages.error('Userprofile with this contact already exists')
#            return render('edit_profile')
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updates successfully')
            return redirect('userprofile')
        else:
            print(form.errors)
            for field in form:
                for error in field.errors:
                    messages.error(request, f'{field.label} : {error}')
                    return redirect('edit_profile')
    
    form = UserProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form':form})


@login_required(login_url="/users/login_user/")
def users(request):

    users = UserProfile.objects.all().order_by('business_name')
    # ToDo user should be able to browse users via the insdustry they work in of type of business the run
    if request.method == 'POST':
        business_type = request.POST.get('business_type')
        industry_type = request.POST.get('industry_type')

        if business_type and industry_type:
            users = UserProfile.objects.filter(Q(business_type=business_type) & Q(industry_type=industry_type)).order_by('business_name')
        elif business_type:
            users = UserProfile.objects.filter(business_type=business_type).order_by('business_name')
        elif industry_type:
            users = UserProfile.objects.filter(industry_type=industry_type).order_by('business_name')

    industries = Industry.objects.all().order_by('name')
    businesses = [choice[0] for choice in UserProfile._meta.get_field('business_type').choices]

    return render(request, 'users/users.html', {
        'users': users,
        'industries': industries,
        'businesses': businesses
    })


@login_required(login_url="/users/login_user/")
def user(request, uid):
    user = CustomUser.objects.get(uid = uid)
    industries = user.profile.industry_type.all()
    return render(request, 'users/user.html', {'user':user, 'industries':industries})
"""
INDUSTRIES = [
    'Aerospace', 'Agriculture', 'Apparel/Textile', 'Automotive', 'Banking', 'Chemical_Manufacturing', 'Construction/Contrating', 'Consulting', 'Consumer_Goods',
    'Defence', 'E_Commerce', 'Education', 'Energy/Oil_Gas', 'Engineering', 'Entertainment', 'Event_Management', 'Food_Beverages', 'Govt/Utilities',
    'Healthcare/Pharma', 'Heavy_Equipment', 'IT/Software/AI', 'Journalism', 'Legal_Services', 'Logistic/Transport', 'Mining', 'Real_Estate', 'Retail', 'Sports', 
    'Telecom', 'Tourism', 'Other'
    ]
BUSINESS_TYPES = ['Trader/WholeSeller/Distributor', 'Manufacturer', 'Service Organization']
"""