from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreate.as_view(), name='project-list-create'),
    path('transactions/', views.TransactionListCreate.as_view(), name='transaction-list-create'),
]
