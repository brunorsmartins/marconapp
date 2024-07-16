from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Project, Transaction
from .forms import ProjectForm, TransactionForm
from django.db.models import Sum
from django.views import View

def home(request):
    total_income = Transaction.objects.filter(is_expense=False).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Transaction.objects.filter(is_expense=True).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses
    return render(request, 'finance/home.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance
    })

def project_list(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')
    else:
        form = ProjectForm()
    projects = Project.objects.all()
    return render(request, 'finance/project_list.html', {'projects': projects, 'form': form})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    transactions = Transaction.objects.filter(project=project)
    total_income = transactions.filter(is_expense=False).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(is_expense=True).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.project = project
            transaction.save()
            return redirect('project-detail', pk=project.pk)
    else:
        form = TransactionForm()
    return render(request, 'finance/project_detail.html', {
        'project': project,
        'transactions': transactions,
        'form': form,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
    })

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project-list')

def transaction_list(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    transactions = Transaction.objects.filter(project__isnull=True)
    return render(request, 'finance/transaction_list.html', {'transactions': transactions, 'form': form})

def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_form.html', {'form': form})

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('transaction-list')
