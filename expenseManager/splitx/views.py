from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
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

def view_profile(request):
    return render(request, 'splitx/profile.html', {'user': request.user})

def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('/splitx/profile')
    else:
        form = UserChangeForm(instance=request.user)
        return render(request, 'splitx/edit_profile.html', {'form': form})
