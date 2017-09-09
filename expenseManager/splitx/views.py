from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from splitx.forms import RegistrationForm

def home(request):
    return render(request, 'splitx/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/splitx/login')
    else:
        form = RegistrationForm()
        return render(request, 'splitx/register_form.html', {'form':form})
    
