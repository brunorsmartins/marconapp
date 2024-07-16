from django import forms
from .models import Project, Transaction

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date', 'is_expense']
