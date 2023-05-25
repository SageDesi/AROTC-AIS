from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from django.http import JsonResponse    
import json

# from .models import Task
from .forms import PositionForm

from .models import *


class CustomLoginView(LoginView):
    template_name = 'CFO/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'CFO/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

def ChartOfAccounts(request):
    Account = COA.objects.order_by('concatenated_id')
    if request.method == "POST":
        AccCatVal = request.POST['AccCat'] #Values are '1' for Asset, '2' for Liability, and so on. AccCatVal is short for Account Category Value
        SubID = request.POST['SubID']
        AccCat = SuperCOA.objects.get(pk=AccCatVal).SuperID_Name
        AccName = request.POST['AccName']
        To_Increase = request.POST['To_Increase']
        AccDescription = request.POST['AccDescription']
        Acc = COA(SuperID=AccCatVal, SubID=SubID, AccountName=AccName, AccountCategory=AccCat, To_Increase=To_Increase, AccountDescription=AccDescription)
        Acc.save()
    return render(request, "CFO/ChartOfAccounts.html", {'Account':Account}) 

# def JournalEntry(request):
#     Account = COA.objects.order_by('concatenated_id')
#     if request.method == "POST":
#         debit = request.POST['debit']
#     return render(request, "CFO/JournalEntry.html", {'Account':Account}) 

class JournalEntry(View):
    def get(self, request):
        accounts = COA.objects.all()
        # Render the form template
        return render(request, 'CFO/JournalEntry.html',{'Account':accounts})

    def post(self, request):
        accounts = COA.objects.all()
        # Retrieve the JSON data from the form submission
        transactions_json = request.POST.get('transactions')

        if transactions_json:
            # Parse the JSON data into a Python list of dictionaries
            transactions = json.loads(transactions_json)

            # Process and save the transactions
            for transaction_data in transactions:
                account = transaction_data.get('account')
                amount = transaction_data.get('amount')
                category = transaction_data.get('category')

                # Create a new Transaction instance and save it
                transaction = Transaction(JournalID=account, TransactionAmount=amount, TransactionCategory=category)
                transaction.save()

        # Redirect to a success page or render a response as needed
        return render(request, 'CFO/JournalEntry.html',{'Account':accounts})

def get_accounts(request):
    accounts = Account.objects.all()

    # Serialize the account data to JSON format
    serialized_accounts = [
        {
            'pk': account.pk,
            'AccountName': account.AccountName
        }
        for account in accounts
    ]

    return JsonResponse(serialized_accounts, safe=False)