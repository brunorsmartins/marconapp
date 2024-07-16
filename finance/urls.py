from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project-delete'),
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/add/', views.transaction_add, name='transaction-add'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction-delete'),
]
