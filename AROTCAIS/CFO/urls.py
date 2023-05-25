from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('ChartOfAccounts/', views.ChartOfAccounts, name='ChartOfAccounts'),
    path('JournalEntry/', JournalEntry.as_view(), name='JournalEntry'),
    path('accounts/', views.get_accounts, name='get_accounts'),
    path('EditAccount/<int:pk>', views.EditAccount, name="EditAccount"),
    path('DeleteAccount/<int:pk>/', views.DeleteAccount, name='DeleteAccount')
]
