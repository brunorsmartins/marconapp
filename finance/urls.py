from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete-project'),
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete-transaction'),
    path('common-expenses/', views.common_expense_list, name='common-expense-list'),
]
