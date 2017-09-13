from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, F

from splitx.forms import RegistrationForm, EditProfileForm, AddExpenseForm
from splitx.models import Expense, Transaction

from collections import defaultdict

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            cost         = form.cleaned_data['cost']
            current_time = timezone.now()
            expense = Expense(
                name       = form.cleaned_data['name'],
                cost       = cost,
                created_by = request.user,
                pub_date   = current_time,
            )
            expense.save()

            paid_by = form.cleaned_data['paid_by']
            paid_to = form.cleaned_data['paid_to']
            cost_paid_by_each_user = int(cost) / len(paid_by)
            for paid_by_user in paid_by:
                cost_owe_by_each_user = cost_paid_by_each_user / len(paid_to)
                for paid_to_user in paid_to:
                    # NOTE: 'paid_by' user can be same as 'paid_to' user,
                    #       this record is required to define completeness of expense.
                    transaction = Transaction(
                        paid_by    = User.objects.get(pk=paid_by_user),
                        paid_to    = User.objects.get(pk=paid_to_user),
                        expense_id = expense,
                        amount     = cost_owe_by_each_user,
                        pub_date   = current_time,
                    ) 
                    transaction.save()

        return redirect('/splitx/')
    else:
        form = AddExpenseForm()
        return render(request, 'splitx/expense_form.html', {'form':form})

def home(request):
    # NOTE: Below code('request.user') will work even when there is no login user,
    #       since django has default login user(Anonymous)
    transactions = get_all_transactions_for_user(request.user)
    owe_to   = defaultdict(int)
    owe_from = defaultdict(int)
    total_owe_to   = 0
    total_owe_from = 0
    for transaction in transactions:
        if transaction.paid_by == request.user:
            owe_from[transaction.paid_to.first_name] += int(transaction.amount)
            total_owe_from += int(transaction.amount)
        else:
            owe_to[transaction.paid_by.first_name] += int(transaction.amount)
            total_owe_to += int(transaction.amount)
    balance = total_owe_to - total_owe_to
    return render(request, 'splitx/home.html', {\
            'transactions':   transactions,\
            'owe_to':         dict(owe_to),\
            'owe_from':       dict(owe_from),\
            'total_owe_to':   total_owe_to,\
            'total_owe_from': total_owe_from,\
            'balance':        balance,
            })

def get_all_transactions_for_user(user):
    # Retrieve all the transactions were current user is involve
    # and ignore transactions were user had paid to himself
    return Transaction.objects.all()\
            .order_by('-pub_date')\
            .filter( (Q(paid_by=user.id) | Q(paid_to=user.id)) & ~Q(paid_by = F('paid_to')) )    

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/splitx/login')
    else:
        form = RegistrationForm()
        return render(request, 'splitx/register_form.html', {'form':form})

@login_required
def view_profile(request):
    return render(request, 'splitx/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('/splitx/profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'splitx/edit_profile.html', {'form': form})

@login_required
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
