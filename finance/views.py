from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum
from rest_framework import generics
from .models import Project, Transaction, CommonExpense
from .serializers import ProjectSerializer, TransactionSerializer
from .forms import ProjectForm, TransactionForm, CommonExpenseForm

# API views
class ProjectListCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# Template views
def home(request):
    current_year = timezone.now().year
    monthly_data = []

    for month in range(1, 13):
        total_expenses = Transaction.objects.filter(date__month=month, date__year=current_year, is_expense=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_income = Transaction.objects.filter(date__month=month, date__year=current_year, is_expense=False).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = float(total_income - total_expenses)  # Convertendo para float
        monthly_data.append(balance)
    
    return render(request, 'finance/home.html', {
        'monthly_data': monthly_data,
        'current_year': current_year,
    })

def project_list(request):
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')
    else:
        form = ProjectForm()
    return render(request, 'finance/project_list.html', {'projects': projects, 'form': form})

def common_expense_list(request):
    expenses = CommonExpense.objects.all()
    if request.method == 'POST':
        form = CommonExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common-expense-list')
    else:
        form = CommonExpenseForm()
    
    return render(request, 'finance/common_expense_list.html', {
        'expenses': expenses,
        'form': form
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    transactions = Transaction.objects.filter(project=project)
    total_income = transactions.filter(is_expense=False).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(is_expense=True).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.project = project
            transaction.save()
            return redirect(reverse('project-detail', args=[pk]))
    else:
        form = TransactionForm()
    
    return render(request, 'finance/project_detail.html', {
        'project': project,
        'transactions': transactions,
        'form': form,
        'balance': balance
    })

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project-list')
    return render(request, 'finance/delete_confirm.html', {'object': project})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('project-detail', pk=transaction.project.pk)
    return render(request, 'finance/delete_confirm.html', {'object': transaction})

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})

def common_expense_list(request):
    common_expenses = Transaction.objects.filter(project__isnull=True)
    return render(request, 'finance/common_expense_list.html', {'common_expenses': common_expenses})

class ProjectListCreate(View):
    def get(self, request):
        projects = Project.objects.all()
        form = ProjectForm()
        return render(request, 'finance/project_list.html', {'projects': projects, 'form': form})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')
        projects = Project.objects.all()
        return render(request, 'finance/project_list.html', {'projects': projects, 'form': form})

def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    transactions = Transaction.objects.filter(project=project)
    return render(request, 'finance/project_detail.html', {'project': project, 'transactions': transactions})

def transaction_list_create(request):
    transactions = Transaction.objects.all()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions, 'form': form})

def common_expense_list(request):
    expenses = CommonExpense.objects.all()
    if request.method == 'POST':
        form = CommonExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common-expense-list')
    else:
        form = CommonExpenseForm()
    return render(request, 'finance/common_expense_list.html', {'expenses': expenses, 'form': form})

def home(request):
    current_month = timezone.now().month
    current_year = timezone.now().year
    total_income = Transaction.objects.filter(date__month=current_month, date__year=current_year, is_expense=False).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(date__month=current_month, date__year=current_year, is_expense=True).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses
    return render(request, 'finance/home.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance
    })