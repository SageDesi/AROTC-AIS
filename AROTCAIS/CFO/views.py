# app/views.py

from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class UserLogin(LoginView):
    template_name = 'app/signin.html'
    fields = '__all__'
    redirect_authenticated_user = True

class UserSignup(FormView):
    template_name = 'app/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pfl-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignup, self).form_valid(form)

    def get(self, *args, **kwargs):
        return super(UserSignup, self).get(*args, **kwargs)