from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from splitx.models import Expense

class AddExpenseForm(forms.Form):
    name = forms.CharField(label='Expense description')
    cost = forms.IntegerField(label='Expense amount')

    friends_ids = []
    for user in User.objects.all():
        friends_ids.append((user.id, user.first_name))
    paid_by = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=friends_ids)
    paid_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=friends_ids)

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
