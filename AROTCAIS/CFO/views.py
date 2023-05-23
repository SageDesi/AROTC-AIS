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

# from .models import Task
from .forms import PositionForm


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
    if request.method == "POST":
        AccCat = request.POST['AccCat']
        To_Increase = request.POST['To_Increase']
        AccDescription = request.POST['AccDescription']
        SuperCoa = SuperCOA(SuperID=AccCat)
        Acc = Product(ProductName=prodname, ProductCost=prodprice, ProductStock=0)
        new_prod.save()
    return render(request, "CFO/ChartOfAccounts.html")