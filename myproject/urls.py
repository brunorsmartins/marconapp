from django.contrib import admin
from django.urls import path
from finance import views as finance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', finance_views.home, name='home'),
    path('api/projects/', finance_views.ProjectListCreate.as_view(), name='project-list'),  # Corrigido aqui
    path('api/projects/<int:pk>/', finance_views.project_detail, name='project-detail'),
    path('api/transactions/', finance_views.transaction_list_create, name='transaction-list'),
    path('common-expenses/', finance_views.common_expense_list, name='common-expense-list'),
]
