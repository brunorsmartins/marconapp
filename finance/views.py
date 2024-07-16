from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Sum
from .models import Project, Transaction
from .forms import ProjectForm, TransactionForm

def home(request):
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    total_expenses = Transaction.objects.filter(date__month=current_month, date__year=current_year, is_expense=True).aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = Transaction.objects.filter(date__month=current_month, date__year=current_year, is_expense=False).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses
    
    return render(request, 'finance/home.html', {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': balance
    })

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'finance/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    transactions = project.transactions.all()
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
        'form': form
    })

def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')
    else:
        form = ProjectForm()
    return render(request, 'finance/project_add.html', {'form': form})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project-list')

def transaction_list(request):
    transactions = Transaction.objects.filter(project__isnull=True)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.project = None
            transaction.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_list.html', {
        'transactions': transactions,
        'form': form
    })

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('transaction-list')

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_form.html', {'form': form})

def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_form.html', {'form': form})