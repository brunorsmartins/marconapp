from django.contrib import admin
from django.urls import path
from finance import views as finance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', finance_views.home, name='home'),
    path('projects/', finance_views.project_list, name='project-list'),
    path('projects/add/', finance_views.project_add, name='project-add'),
    path('projects/<int:pk>/', finance_views.project_detail, name='project-detail'),
    path('projects/<int:pk>/delete/', finance_views.project_delete, name='project-delete'),
    path('transactions/', finance_views.transaction_list, name='transaction-list'),
    path('transactions/<int:pk>/delete/', finance_views.transaction_delete, name='transaction-delete'),
]
