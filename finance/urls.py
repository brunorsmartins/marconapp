from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),
]
