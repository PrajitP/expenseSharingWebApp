from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from splitx.forms import RegistrationForm, EditProfileForm

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
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('/splitx/profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'splitx/edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            # NOTE: 'request.user' will be set to anonomus after 'save()', 'form.user' is one whose password got changed
            update_session_auth_hash(request, form.user)
            return redirect('/splitx/profile')
        else:
            return redirect('/splitx/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'splitx/change_password.html', {'form': form})

