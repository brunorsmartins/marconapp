from django.shortcuts import render
from rest_framework import generics
from .models import Project, Transaction
from .serializers import ProjectSerializer, TransactionSerializer

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
    return render(request, 'finance/home.html')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'finance/project_list.html', {'projects': projects})

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})
