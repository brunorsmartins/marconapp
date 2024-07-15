from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def total_transactions(self):
        total = self.transactions.aggregate(total=models.Sum('amount'))['total']
        return total if total else 0

    def __str__(self):
        return self.name

class Transaction(models.Model):
    project = models.ForeignKey(Project, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    is_expense = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
