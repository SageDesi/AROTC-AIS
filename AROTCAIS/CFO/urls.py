from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('ChartOfAccounts/', views.ChartOfAccounts, name='ChartOfAccounts'),
    path('JournalEntry/', views.JournalEntry, name='JournalEntry'),
    path('addJournalEntry/', views.addJournalEntry, name='addJournalEntry'),
    path('EditAccount/<int:pk>', views.EditAccount, name="EditAccount"),
    path('DeleteAccount/<int:pk>/', views.DeleteAccount, name='DeleteAccount')
]
