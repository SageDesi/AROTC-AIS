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
from django.http import JsonResponse    
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
