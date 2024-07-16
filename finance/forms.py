from django import forms
from .models import Project, Transaction

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        labels = {
            'name': 'Nome',
            'description': 'Descrição'
        }
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'description': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class TransactionForm(forms.ModelForm):
    expense_or_income = forms.ChoiceField(
        choices=[(True, 'Despesa'), (False, 'Receita')],
        widget=forms.RadioSelect,
        label='Tipo'
    )

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date', 'expense_or_income']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'date': forms.TextInput(attrs={'class': 'datepicker form-control', 'autocomplete': 'off'}),
        }
        labels = {
            'description': 'Descrição',
            'amount': 'Quantia',
            'date': 'Data',
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_expense = self.cleaned_data['expense_or_income'] == 'True'
        if commit:
            instance.save()
        return instance
