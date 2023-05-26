from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
import xml.etree.ElementTree as ET
from django.http import HttpResponseBadRequest, JsonResponse
import json

# from .models import Task
from .forms import PositionForm

from .models import *
from .models import COA

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

def JournalEntry(request):
    accounts = COA.objects.all()
    # Render the form template with accounts data
    return render(request, 'CFO/JournalEntry.html', {'Account': accounts})

def addJournalEntry(request):
    if request.method == "POST":
        content_type = request.META.get('CONTENT_TYPE')

        if content_type == 'application/json':
            # Handle JSON request
            json_data = json.loads(request.body)
            debited_accounts = json_data.get('debitedAccounts')
            credited_accounts = json_data.get('creditedAccounts')
        elif content_type == 'application/xml':
            # Handle XML request
            xml_data = request.body
            xml_root = ET.fromstring(xml_data)
            debited_accounts = {}
            credited_accounts = {}

            for account_element in xml_root.iter('account'):
                account_id = account_element.get('id')
                amount = float(account_element.text or 0)

                if account_element.get('type') == 'debited':
                    debited_accounts[account_id] = amount
                elif account_element.get('type') == 'credited':
                    credited_accounts[account_id] = amount
                else:
                    return HttpResponseBadRequest("Invalid XML data")

        else:
            return HttpResponseBadRequest("Unsupported content type")

        if debited_accounts and credited_accounts:
            # Rest of your code for saving the journal entry

            # Return a JSON response to indicate success
            response_data = {'message': 'Data saved successfully'}
            return JsonResponse(response_data)
        else:
            # Return a JSON response to indicate an error
            response_data = {'message': 'Invalid data'}
            return JsonResponse(response_data, status=400)

    else:
        return HttpResponseBadRequest("Invalid request method")

def EditAccount(request,pk):
    AccDetails = COA.objects.get(pk=pk)
    
    if(request.method == "POST"):
        AccCatVal = request.POST['AccCat'] #Values are '1' for Asset, '2' for Liability, and so on. AccCatVal is short for Account Category Value
        SubID = request.POST['SubID']
        AccCat = SuperCOA.objects.get(pk=AccCatVal).SuperID_Name
        AccName = request.POST['AccName']
        To_Increase = request.POST['To_Increase']
        AccDescription = request.POST['AccDescription']

        if SubID == "" or AccCat == "" or AccName == "" or To_Increase == "" or AccDescription == "" :
            messages.warning(request,"One or more fields are empty!")
            return redirect("EditAccount", pk=pk) 
        else:
            COA.objects.filter(pk=pk).update(SubID = SubID, AccountCategory = AccCat, AccountName=AccName, To_Increase=To_Increase, AccountDescription=AccDescription)
            messages.success(request, 'Account Updated!')
            
            return redirect('ChartOfAccounts')

    else:
        return render(request, 'CFO/EditAccount.html', {'acc':AccDetails}) 

def DeleteAccount(request, pk):
    item.objects.filter(pk=pk).delete()
    messages.warning(request,"Item Deleted!")
    return redirect('ChartOfAccounts')
