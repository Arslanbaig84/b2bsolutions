from django.shortcuts import render
from .forms import CustomUserForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
    
    form = CustomUserForm()
    return render(request, 'users/register.html', {'form':form})